# Crop and zoom a region of a PNG without image libraries: pngcrop.py in.png out.png x y w h zoom
import sys, zlib, struct
def read_png(p):
    d=open(p,'rb').read(); assert d[:8]==b'\x89PNG\r\n\x1a\n'
    pos=8; idat=b''; w=h=0; ct=0
    while pos<len(d):
        ln,=struct.unpack('>I',d[pos:pos+4]); typ=d[pos+4:pos+8]; body=d[pos+8:pos+8+ln]; pos+=12+ln
        if typ==b'IHDR': w,h,bd,ct=struct.unpack('>IIBB',body[:10])
        elif typ==b'IDAT': idat+=body
    bpp={2:3,6:4}[ct]; raw=zlib.decompress(idat); stride=w*bpp; out=[]; prev=bytearray(stride); i=0
    for y in range(h):
        f=raw[i]; line=bytearray(raw[i+1:i+1+stride]); i+=1+stride
        for x in range(stride):
            a=line[x-bpp] if x>=bpp else 0; b=prev[x]; c=prev[x-bpp] if x>=bpp else 0
            if f==1: line[x]=(line[x]+a)&255
            elif f==2: line[x]=(line[x]+b)&255
            elif f==3: line[x]=(line[x]+(a+b)//2)&255
            elif f==4:
                pa=abs(b-c); pb=abs(a-c); pc=abs(a+b-2*c)
                pr=a if pa<=pb and pa<=pc else (b if pb<=pc else c); line[x]=(line[x]+pr)&255
        out.append(bytes(line)); prev=line
    return w,h,bpp,out
def write_png(p,w,h,bpp,rows):
    ct={3:2,4:6}[bpp]; raw=b''.join(b'\x00'+r for r in rows)
    def chunk(t,b): return struct.pack('>I',len(b))+t+b+struct.pack('>I',zlib.crc32(t+b)&0xffffffff)
    open(p,'wb').write(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,ct,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
src,dst,x0,y0,cw,ch,z=sys.argv[1],sys.argv[2],*map(int,sys.argv[3:8])
w,h,bpp,rows=read_png(src)
out=[]
for y in range(y0,y0+ch):
    r=rows[y][x0*bpp:(x0+cw)*bpp]; zr=b''.join(r[i*bpp:(i+1)*bpp]*z for i in range(cw))
    for _ in range(z): out.append(zr)
write_png(dst,cw*z,ch*z,bpp,out); print("wrote",dst)
