
#     when problem in h5
# pip3 install --upgrade tables
# pip3 install hd5
# apt  install  lbzip2
# apt  install
# apt  install p7zip-full
#
import pandas as pd
import subprocess as sp
import os
#import click
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
#import h5py

import sys
import subprocess

from fire import Fire


comps=['pixz','pbzip2','lbzip2','pigz','zstd','7z']
# pbzip is bad with image... very long time
comps=['pixz','lbzip2','pigz','zstd','7z']






FILESIZE=-1

def file_size(file_path):
    """
    this function will return the file size
    """
    global FILESIZE
    #if FILESIZE>=0:
    #    return FILESIZE
    if os.path.isfile(file_path):
        #print("D... finding file size")
        #print("D... isfile")
        file_info = os.stat(file_path)
        #print( file_info.st_size)
        FILESIZE=file_info.st_size
    else:
        #print("D... I assume it is a FOLDER")
        out=subprocess.check_output(['du','-bs', file_path ])
        #print(out)
        FILESIZE= out.split()[0].decode('utf-8')
        FILESIZE=int(FILESIZE)
    #print("D.... Size=",FILESIZE)
    #quit()
    return FILESIZE






def get_max_level(code):
    if code=="xz" or code=="pixz":
        return 9
    elif code=="pbzip2" or code=="bzip2":
        return 9
    elif code=="lbzip2":
        return 9
    elif code=="pigz" or code=="gzip":
        return 9
    elif code=="zstd":
        return 19
    elif code=="7z":
        return 9
    else:
        print("!... not known compressor")
        quit()

def get_ext(code):
    if code=="xz" or code=="pixz":
        return 'xz'
    elif code=="pbzip2" or code=="bzip2":
        return 'bz2'
    elif code=="lbzip2":
        return 'lbz2'
    elif code=="pigz" or code=="gzip":
        return 'gz'
    elif code=="zstd":
        return 'zst'
    elif code=="7z":
        return '7z'
    else:
        print("!... not known compressor")
        quit()


#@click.command()
#@click.argument('filename')
#@click.option('--code', '-c')
#@click.option('--level', '-l' ,default=1 )
def compfile( filename, code , level=1 , show_only=False):
    if filename[-1]=="/":
            filename = filename[:-1]

    size=file_size( filename )
    ext=get_ext(code)
    OUTFILE="{}.{}.tar.{}".format(  filename,level,ext )
    OUTFILE=os.path.split(OUTFILE)[-1]

    if code=="xz" or code=="pixz":
#        code="pxz --stdout -"+str(level)+" > "+OUTFILE
        code="pixz -"+str(level)+" > "+OUTFILE

    elif code=="pbzip2" or code=="bzip2":
        code="pbzip2 --stdout -"+str(level)+" > "+OUTFILE

    elif code=="lbzip2":
        code="lbzip2 --stdout -"+str(level)+" > "+OUTFILE

    elif code=="pigz" or code=="gzip":
        code="pigz --stdout -"+str(level)+" > "+OUTFILE

    elif code=="zstd":
        code="zstd -T0 --stdout -"+str(level)+" > "+OUTFILE

    elif code=="7z":
        code="7z a -si  -mx"+str(level)+" "+OUTFILE

    else:
        print("!... not known compressor")
        sys.exit(1)



    #CMD="cat {} | pv -s {} -r -e -p -t | {}  ".format(
    CMD="tar -c {} | pv -s {} -r -e -p -t | {}  ".format(
        filename ,
        size ,
        code)

    if show_only:
        print(CMD)
        return
    print(CMD)


    start=dt.datetime.now()
    sp.getoutput( CMD )
    stop=dt.datetime.now()


    X= (stop-start).total_seconds()
    print(OUTFILE, filename)
    print("D... ratio = {} /  {} ".format( file_size( OUTFILE ) , file_size( filename ) ) )
    Y=100*file_size( OUTFILE )/file_size( filename )
    #print( X)
    print( "{:10s}  {:2d}    {:6.1f}  {:3.1f} %".format( code.split()[0], level, X, Y ) )
    #  from 2021 -  level must be float not int
    return code.split()[0], float(level), float(X), float(Y)
#===========compfile end==================




#---------------------
def compress(FILE, WHAT=''):
    #FILE='forecast'
    #FILE='aaa'

    for co in comps:
        for i in range(1,get_max_level(co)+1 ):
            compfile( FILE  , co, i   , show_only=True)
    print("D.... add 'test' to the command line  to run all compressions!!!")

    print("i... max comp choice and medium comp with fast decompression:")
    compfile( FILE  , "pixz", 9   , show_only=True)
    compfile( FILE  , "zstd", 10   , show_only=True)


    if WHAT != "test":
        sys.exit(0)




    df = pd.DataFrame( [], columns = ['time','ratio','code','level'] )

    ax = plt.gca()

    row=0
    for co in comps:
        for i in range(1,get_max_level(co)+1 ):

            code,level,x,y=compfile( FILE  , co, i   )
            print("D.. {} {} {} {}".format(code,level,x,y) )

            df.loc[row]=[x,y,code,level]
            row=row+1
            #print("D...",df)
        pie=df[df.code==co].plot( style=".-",x='time',y='ratio', label=co,ax=ax)




    filename='compressed_results.h5'
    key="comp_"+FILE
    key = key.replace(".","_")
    #    df.to_hdf(filename, key , table=True, mode='a')
    #print("\n\nD... {} {} \n\n".format( filename, key) )

    #    df.to_hdf(filename, key , format='table', mode='a')
    #print(df.dtypes)
    df.to_hdf(filename, key , format='table', mode='a')

    fig = pie.get_figure()
    fig.savefig("comp.png")
    #    plt.show()
    #    plt.savefig("comp.png")


    # print("D... VISIT LINE ======================+++")
    # with h5py.File(filename,'r') as hf:
    #     hf.visit(print)


    f=pd.read_hdf(filename,key)
    print("D... ========================= rpint hdf==========")
    print(f)


def decompress(FILE):
    print("D... decompress placeholder", FILE)
    ex = os.path.splitext(FILE)[-1]
    #print(ex)
    CMD = "echo Nocommand"
    if ex == ".zst":
        CMD = "zstd -d --stdout "+FILE+" > /dev/null"
    elif ex == ".7z":
        CMD = "7z x -so  "+FILE+" > /dev/null"
    elif ex == ".gz":
        CMD = "gunzip -d -c  "+FILE+" > /dev/null"
    elif ex == ".xz":
        CMD = "xz --decompress --stdout  "+FILE+" > /dev/null"
    elif ex == ".lbz2":
        CMD = "lbzip2 --decompress --stdout  "+FILE+" > /dev/null"

    print(CMD)
    start=dt.datetime.now()
    sp.getoutput( CMD )
    stop=dt.datetime.now()

    X= (stop-start).total_seconds()
    print("{}  {:5.0f} sec.  {}".format(ex, X, FILE))


######################################################
#
#
#
#######################################################
#
#
#
####################################################

if (__name__ == "__main__" ):
    help="""i... BEST CHOICES:
 9.xz    Best compression (and faster than 7z) -
10.zst   Medium compression - lightning decompression
pixz     max and fast for RPi images

"""
    print(help)

    Fire({'c':compress,
          'd':decompress
    })
    print(help)
