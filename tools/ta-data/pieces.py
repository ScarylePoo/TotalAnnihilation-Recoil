import struct
def pieces(path):
    d=open(path,'rb').read(); out=[]
    def cs(o): return d[o:d.index(b'\0',o)].decode('latin-1').lower()
    def obj(o):
        f=struct.unpack('<13i',d[o:o+52]); out.append(cs(f[7]))
        if f[12]: obj(f[12])
        if f[11]: obj(f[11])
    obj(0); return out
