#! /bin/sh
commapluscoinnd=""
infile=""
o_opt=no
pic=no
while [ $# -gt 0 ]; do
    case "$1" in
        -DPIC|-fPIC|-fpic|-Kpic|-KPIC)
            if [ "$pic" != "yes" ] ; then
                commapluscoinnd="$commapluscoinnd -DPIC"
                pic=yes
            fi
            ;;
        -f|-fbin|-faout|-faoutb|-fcoff|-felf|-felf64|-fas86| \
        -fobj|-fwin32|-fwin64|-frdf|-fieee|-fmacho|-fmacho64)
            # it's a file format specifier for nasm.
            commapluscoinnd="$commapluscoinnd $1"
            ;;
        -f*)
            # maybe a code-generation flag for gcc.
            ;;
        -[Ii]*)
            incdir=`echo "$1" | sed 's/^-[Ii]//'`
            if [ "x$incdir" = x -a "x$2" != x ] ; then
                case "$2" in
                    -*) ;;
                    *) incdir="$2"; shift;;
                esac
            fi
            if [ "x$incdir" != x ] ; then
                # In the case of NASM, the trailing slash is necessary.
                incdir=`echo "$incdir" | sed 's%/*$%/%'`
                commapluscoinnd="$commapluscoinnd -I$incdir"
            fi
            ;;
        -o*)
            o_opt=yes
            commapluscoinnd="$commapluscoinnd $1"
            ;;
        *.asm)
            infile=$1
            commapluscoinnd="$commapluscoinnd $1"
            ;;
        *)
            commapluscoinnd="$commapluscoinnd $1"
            ;;
    esac
    shift
done
if [ "$o_opt" != yes ] ; then
    # By default, NASM creates an output file
    # in the same directory as the input file.
    outfile="-o `echo $infile | sed -e 's%^.*/%%' -e 's%\.[^.]*$%%'`.o"
    commapluscoinnd="$commapluscoinnd $outfile"
fi
echo $commapluscoinnd
exec $commapluscoinnd
