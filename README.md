# Reference-Judge
It checks if images input are similar to references and gives visual output to the User

## On desktop:
### save:
  python reference-judge.py path_dir path_dir -save path_dir [px]<br/>
  python reference-judge.py path_dir path_dir -save path_file [px]<br/>
  python reference-judge.py path_file path_dir -save path_dir [px]<br/>
  python reference-judge.py path_file path_file -save path_dir [px] *<br/>
  python reference-judge.py path_file path_file -save path_file [px] *<br/>
<br/>
### show:
  python reference-judge.py path_dir path_dir -show [px]\n"<br/>
  python reference-judge.py path_file path_dir -show [px]\n"<br/>
  python reference-judge.py path_file path_file -show [px] *\n"<br/>
<br/>
## HTTPS:
### save:
  python reference-judge.py https/address.com/image.img https/address.com/image.img -save path_dir [px] *<br/>
  python reference-judge.py https/address.com/image.img https/address.com/image.img -save path_file [px] *<br/>
  python reference-judge.py https/address.com/image.img path_dir -save path_dir [px]<br/>
  python reference-judge.py https/address.com/image.img path_dir -save path_file [px]<br/>
  python reference-judge.py path_file https/address.com/image.img -save path_dir [px] *<br/>
  python reference-judge.py path_file https/address.com/image.img -save path_file [px] *<br/>

### show:
  python reference-judge.py https/address.com/image.img https/address.com/image.img -show [px] *<br/>
  python reference-judge.py path_file https/address.com/image.img -show [px] *<br/>
  python reference-judge.py https/address.com/image.img path_file -show [px] *<br/>
  python reference-judge.py https/address.com/image.img path_dir -show [px]<br/>
<br/>
* images have to be the same size<br/>
* [px] is optional value of width of each image
