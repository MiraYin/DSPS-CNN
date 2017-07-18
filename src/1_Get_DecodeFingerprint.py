import string
import binascii
import urllib2

_lsb_bit_table = {}
_msb_bit_table = {}

_reverse_bits_in_a_byte_transtable = None

_lsb_4bit_patterns = (
    "0000", "1000", "0100", "1100",
    "0010", "1010", "0110", "1110",
    "0001", "1001", "0101", "1101",
    "0011", "1011", "0111", "1111")

# Generate '00000000', '10000000', '01000000', ... , '01111111', '11111111'
def _lsb_8bit_patterns():
    for right in _lsb_4bit_patterns:
        for left in _lsb_4bit_patterns:
            yield left + right

def _init():
    to_trans = [None]*256
    for value, bit_pattern in enumerate(_lsb_8bit_patterns()):
        # Each pattern maps to the byte
        byte_value = chr(value)
        to_trans[value] = chr(int(bit_pattern, 2))

        _lsb_bit_table[bit_pattern] = byte_value
        # Include the forms with trailing 0s
        # 10000000, 1000000, 100000, 10000, 1000, 100, 10 and 1 are all 0x01
        # (RDKit fingerprint lengths don't need to be a multiple of 8)
        lsb_pattern = bit_pattern
        while lsb_pattern[-1:] == "0":
            lsb_pattern = lsb_pattern[:-1]
            _lsb_bit_table[lsb_pattern] = byte_value

        msb_pattern = bit_pattern[::-1]
        _msb_bit_table[msb_pattern] = byte_value
        while msb_pattern[:1] == "0":
            msb_pattern = msb_pattern[1:]
            _msb_bit_table[msb_pattern] = byte_value
    global _reverse_bits_in_a_byte_transtable
    _reverse_bits_in_a_byte_transtable = string.maketrans(
        "".join(chr(i) for i in range(256)),
        "".join(to_trans))
    

_init()
assert _lsb_bit_table["10000000"] == "\x01", _lsb_bit_table["10000000"]
assert _lsb_bit_table["1000000"] == "\x01", _lsb_bit_table["1000000"]
assert _lsb_bit_table["100000"] == "\x01"
assert _lsb_bit_table["10000"] == "\x01"
assert _lsb_bit_table["1"] == "\x01"
assert _lsb_bit_table["1111111"] == "\x7f"

assert _msb_bit_table["00000001"] == "\x01"
assert _msb_bit_table["0000001"] == "\x01"
assert _msb_bit_table["000001"] == "\x01"
assert _msb_bit_table["00001"] == "\x01"
assert _msb_bit_table["1"] == "\x01"
assert _msb_bit_table["00000011"] == "\x03"
assert _msb_bit_table["00000011"] == "\x03"
assert _msb_bit_table["10000000"] == "\x80"
assert _msb_bit_table["1000000"] == "\x40"


def from_cactvs(text):
    """Decode a 881-bit CACTVS-encoded fingerprint used by PubChem

    >>> from_cactvs("AAADceB7sQAEAAAAAAAAAAAAAAAAAWAAAAAwAAAAAAAAAAABwAAAHwIYAAAADA" +
    ...             "rBniwygJJqAACqAyVyVACSBAAhhwIa+CC4ZtgIYCLB0/CUpAhgmADIyYcAgAAO" +
    ...             "AAAAAAABAAAAAAAAAAIAAAAAAAAAAA==")
    (881, '\\x07\\xde\\x8d\\x00 \\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x80\\x06\\x00\\x00\\x00\\x0c\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x80\\x03\\x00\\x00\\xf8@\\x18\\x00\\x00\\x000P\\x83y4L\\x01IV\\x00\\x00U\\xc0\\xa4N*\\x00I \\x00\\x84\\xe1@X\\x1f\\x04\\x1df\\x1b\\x10\\x06D\\x83\\xcb\\x0f)%\\x10\\x06\\x19\\x00\\x13\\x93\\xe1\\x00\\x01\\x00p\\x00\\x00\\x00\\x00\\x00\\x80\\x00\\x00\\x00\\x00\\x00\\x00\\x00@\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00')
    >>>

    For format details, see
      ftp://ftp.ncbi.nlm.nih.gov/pubchem/specifications/pubchem_fingerprints.txt
    """
    fp = text.decode("base64")
    # first 4 bytes are the length (struct.unpack(">I"))
    if fp[:4] != '\x00\x00\x03q':
        raise ValueError("This implementation is hard-coded for 881 bit CACTVS fingerprints")
    return 881, fp[4:].translate(_reverse_bits_in_a_byte_transtable)

def get_fingerprint(cid):
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/' + str(cid) + '/record/SDF/?record_type=2d&response_type=display'
    try:
        response = urllib2.urlopen(url)
    except urllib2.URLError, e:    
        print e.reason
        return
    else:
        html = response.read()
        data = html.split("> <PUBCHEM_CACTVS_SUBSKEYS>")[1].split("> <PUBCHEM_IUPAC_OPENEYE_NAME>")[0]
        data = data.strip()
        l, fp = from_cactvs(data)
        assert l == 881
        assert len(fp) == 111
        comp = '00000000'
        out = ''
        for i in range(len(fp)):
            temp = bin(ord(fp[i])).replace('0b','')
            temp = comp[:8-len(temp)]+temp
            temp = temp[::-1]
            out += temp
        return out[:-7]

if __name__ == '__main__':
    os.mkdir("../data/fingerprint")
    f = open("../data/unique_drug.txt",'r')
    lines = f.readlines()
    f.close()
    errList_drug = []
    for line in lines:
        cid = line.strip()
        try:
            fp = get_fingerprint(cid)
        except:
            print cid + ": not found!"
            errList_drug.append(cid)
        else:
            f = open("../data/fingerprint/"+cid+".txt",'w')
            f.write(fp)
            f.close()

    f = open("../data/errorList_drug_cid.txt",'w')
    for in_ in errList_drug:
        f.write(in_+'\n')
    f.close()
