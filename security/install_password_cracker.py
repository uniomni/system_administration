"""Install password cracker John The Ripper

This is based on http://pka.engr.ccny.cuny.edu/~jmao/node/26

Must be run as root or with sudo:

sudo python install_password_cracker.py

To run the cracker do
sudo /usr/local/jrt/john /etc/shadow

and
sudo /usr/local/jrt/john --show /etc/shadow


Modify /usr/local/jrt/john.conf to have

Wordlist = $JOHN/<new wordlist.lst>

See http://www.openwall.com/john/doc/EXAMPLES.shtml
"""

import os
from config import john_home, package_name
from utilities import run, makedir, header, replace_string_in_file



def install_ubuntu_packages():    
    """Get required Ubuntu packages for shakemap.
       It is OK if they are already installed
    """

    header('Installing Ubuntu packages')               
    for package in ['pgpgpg',
                    ]:

                    
        s = 'apt-get -y install %s' % package
        
        log_base = '%s_install' % package
        try:
            run(s,
                stdout=log_base + '.out',
                stderr=log_base + '.err',                  
                verbose=True)
        except:
            msg = 'Installation of package %s failed. ' % package
            msg += 'See log file %s.out and %s.err for details' % (log_base, log_base)
            raise Exception(msg)
            



def download_john_source(john_home):    
    makedir(john_home)
    os.chdir(john_home)

    print 'Current working dir', os.getcwd()

    # Clean out
    s = '/bin/rm -rf %s/*' % john_home
    run(s, verbose=True)

    # Get source and verification
    files = ['http://www.openwall.com/john/g/%s.tar.gz' % package_name,
             'http://www.openwall.com/john/g/%s.tar.gz.sign' % package_name,
             'http://www.openwall.com/signatures/openwall-signatures.asc']
                     
    for file in files:
        path = os.path.join(john_home, file)

        s = 'wget %s' % file
        run(s, verbose=True)

def verify_signature(john_home):                         
    # Verify signature
    os.chdir(john_home)
    print 'Current working dir', os.getcwd()
    
    s = 'pgp -ka openwall-signatures.asc'
    run(s, verbose=True)

    s = 'pgp %s.tar.gz.sign %s.tar.gz' % (package_name, package_name)
    run(s, verbose=True)    

    
def patch_and_compile(john_home):
    os.chdir(john_home)
    
    s = 'tar -xvzf %s.tar.gz' % package_name
    run(s, verbose=True)        
       
    os.chdir(os.path.join(john_home, package_name, 'src'))    
    print 'Current working dir', os.getcwd()
        
    replace_string_in_file('Makefile', 
                           'LDFLAGS = -s', 
                           'LDFLAGS = -s -lcrypt', verbose=True)
                           
    replace_string_in_file('Makefile', 
                           'unique.o', 
                           'unique.o crypt_fmt.o', verbose=True)                           
                           
                           
    replace_string_in_file('john.c', 
                           'extern struct fmt_main fmt_AFS, fmt_LM;',
                           'extern struct fmt_main fmt_AFS, fmt_LM;\nextern struct fmt_main fmt_crypt;',
                           verbose=True)
                           
    replace_string_in_file('john.c', 
                           'john_register_one(&fmt_LM);',
                           'john_register_one(&fmt_LM); john_register_one(&fmt_crypt);',
                           verbose=True)                           
                           
                           


    # Create new
    fid = open('crypt_fmt.c', 'w')
    fid.write("""
/* public domain proof-of-concept code by Solar Designer */

#define _XOPEN_SOURCE /* for crypt(3) */
#include <string.h>
#include <unistd.h>

#include "arch.h"
#include "params.h"
#include "formats.h"

#define FORMAT_LABEL			"crypt"
#define FORMAT_NAME			"generic crypt(3)"
#define ALGORITHM_NAME			"?/" ARCH_BITS_STR

#define BENCHMARK_COMMENT		""
#define BENCHMARK_LENGTH		0

#define PLAINTEXT_LENGTH		72

#define BINARY_SIZE			128
#define SALT_SIZE			BINARY_SIZE

#define MIN_KEYS_PER_CRYPT		1
#define MAX_KEYS_PER_CRYPT		1

static struct fmt_tests tests[] = {
	{"CCNf8Sbh3HDfQ", "U*U*U*U*"},
	{"CCX.K.MFy4Ois", "U*U***U"},
	{"CC4rMpbg9AMZ.", "U*U***U*"},
	{"XXxzOu6maQKqQ", "*U*U*U*U"},
	{"SDbsugeBiC58A", ""},
	{NULL}
};

static char saved_key[PLAINTEXT_LENGTH + 1];
static char saved_salt[SALT_SIZE];
static char *crypt_out;

static int valid(char *ciphertext)
{
#if 1
	int l = strlen(ciphertext);
	return l >= 13 && l < BINARY_SIZE;
#else
/* Poor load time, but more effective at rejecting bad/unsupported hashes */
	char *r = crypt("", ciphertext);
	int l = strlen(r);
	return
	    !strncmp(r, ciphertext, 2) &&
	    l == strlen(ciphertext) &&
	    l >= 13 && l < BINARY_SIZE;
#endif
}

static void *binary(char *ciphertext)
{
	static char out[BINARY_SIZE];
	strncpy(out, ciphertext, sizeof(out)); /* NUL padding is required */
	return out;
}

static void *salt(char *ciphertext)
{
	static char out[SALT_SIZE];
	int cut = sizeof(out);

#if 1
/* This piece is optional, but matching salts are not detected without it */
	switch (strlen(ciphertext)) {
	case 13:
	case 24:
		cut = 2;
		break;

	case 20:
		if (ciphertext[0] == '_') cut = 9;
		break;

	case 34:
		if (!strncmp(ciphertext, "$1$", 3)) {
			char *p = strchr(ciphertext + 3, '$');
			if (p) cut = p - ciphertext;
		}
		break;

	case 59:
		if (!strncmp(ciphertext, "$2$", 3)) cut = 28;
		break;

	case 60:
		if (!strncmp(ciphertext, "$2a$", 4)) cut = 29;
		break;
	}
#endif

	/* NUL padding is required */
	memset(out, 0, sizeof(out));
	memcpy(out, ciphertext, cut);

	return out;
}

static int binary_hash_0(void *binary)
{
	return ((unsigned char *)binary)[12] & 0xF;
}

static int binary_hash_1(void *binary)
{
	return ((unsigned char *)binary)[12] & 0xFF;
}

static int binary_hash_2(void *binary)
{
	return
	    (((unsigned char *)binary)[12] & 0xFF) |
	    ((int)(((unsigned char *)binary)[11] & 0xF) << 8);
}

static int get_hash_0(int index)
{
	return (unsigned char)crypt_out[12] & 0xF;
}

static int get_hash_1(int index)
{
	return (unsigned char)crypt_out[12] & 0xFF;
}

static int get_hash_2(int index)
{
	return
	    ((unsigned char)crypt_out[12] & 0xFF) |
	    ((int)((unsigned char)crypt_out[11] & 0xF) << 8);
}

static int salt_hash(void *salt)
{
	int pos = strlen((char *)salt) - 2;

	return
	    (((unsigned char *)salt)[pos] & 0xFF) |
	    ((int)(((unsigned char *)salt)[pos + 1] & 3) << 8);
}

static void set_salt(void *salt)
{
	strcpy(saved_salt, salt);
}

static void set_key(char *key, int index)
{
	strcpy(saved_key, key);
}

static char *get_key(int index)
{
	return saved_key;
}

static void crypt_all(int count)
{
	crypt_out = crypt(saved_key, saved_salt);
}

static int cmp_all(void *binary, int count)
{
	return !strcmp((char *)binary, crypt_out);
}

static int cmp_exact(char *source, int index)
{
	return 1;
}

struct fmt_main fmt_crypt = {
	{
		FORMAT_LABEL,
		FORMAT_NAME,
		ALGORITHM_NAME,
		BENCHMARK_COMMENT,
		BENCHMARK_LENGTH,
		PLAINTEXT_LENGTH,
		BINARY_SIZE,
		SALT_SIZE,
		MIN_KEYS_PER_CRYPT,
		MAX_KEYS_PER_CRYPT,
		FMT_CASE | FMT_8_BIT,
		tests
	}, {
		fmt_default_init,
		valid,
		fmt_default_split,
		binary,
		salt,
		{
			binary_hash_0,
			binary_hash_1,
			binary_hash_2
		},
		salt_hash,
		set_salt,
		set_key,
		get_key,
		fmt_default_clear_keys,
		crypt_all,
		{
			get_hash_0,
			get_hash_1,
			get_hash_2
		},
		cmp_all,
		cmp_all,
		cmp_exact
	}
};
""")
    fid.close()

    # Now compile the code (64 bit Ubuntu)
    s = 'make linux-x86-64'   
    run(s, verbose=True)
    
    # Copy runfile to system
    os.chdir(os.path.join(john_home, package_name))    
    s = 'cp -pr run /usr/local/jrt'
    run(s, verbose=True)
    print 'john the ripper is now available in /usr/local/jrt'
    print 'To use:'
    print 'sudo /usr/local/jrt/john /etc/shadow'
        
if __name__ == '__main__':

    john_home = os.path.expanduser(john_home) 
    john_home = os.path.join(john_home, 'jtr')

    install_ubuntu_packages()
    download_john_source(john_home)
    verify_signature(john_home)    
    
    patch_and_compile(john_home)
    
