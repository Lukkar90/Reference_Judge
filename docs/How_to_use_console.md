# Usage

python reference-judge.py &lt;source_reference_path&gt; &lt;target_reference_path&gt; <--mode> [directory_diffrences_output] [width]

## Images on hard drive:

### save:

python reference-judge.py path_dir path_dir --save path_dir [px] [-br]<br/>
python reference-judge.py path_dir path_dir --save path_file [px] [-br]<br/>
python reference-judge.py path_file path_dir --save path_dir [px] [-br]<br/>
python reference-judge.py path_file path_file --save path_dir [px] [-br]<br/>
python reference-judge.py path_file path_file --save path_file [px] [-br]<br/>
<br/>

### show:

python reference-judge.py path_dir path_dir --show [px] [-br]<br/>
python reference-judge.py path_file path_dir --show [px] [-br]<br/>
python reference-judge.py path_file path_file --show [px] [-br]<br/>
<br/>

## Images HTTPS:

### save:

python reference-judge.py https/address.com/image.img https/address.com/image.img --save path_dir [px] [-br]<br/>
python reference-judge.py https/address.com/image.img https/address.com/image.img --save path_file [px] [-br]<br/>
python reference-judge.py https/address.com/image.img path_dir --save path_dir [px] [-br]<br/>
python reference-judge.py https/address.com/image.img path_dir --save path_file [px] [-br]<br/>
python reference-judge.py path_file https/address.com/image.img --save path_dir [px] [-br]<br/>
python reference-judge.py path_file https/address.com/image.img --save path_file [px] [-br] 

### show:

python reference-judge.py https/address.com/image.img https/address.com/image.img --show [px] [-br]<br/>
python reference-judge.py path_file https/address.com/image.img --show [px] [-br]<br/>
python reference-judge.py https/address.com/image.img path_file --show [px] [-br]<br/>
python reference-judge.py https/address.com/image.img path_dir --show [px] [-br]<br/>
<br/>

- images have to be the same size<br/>
- [px] is an optional value of the width of each image
- [-br] is an optional mode in which you match images with similar sizes and the same ratio, not recommended due to image distortions
