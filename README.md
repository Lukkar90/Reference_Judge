# Reference-Judge
It checks if images input are similar to references and gives visual output to the User

## On desktop:
### save:
  python {program_name} path_dir path_dir -save path_dir [px]\n"
  python {program_name} path_dir path_dir -save path_file [px]\n"
  python {program_name} path_file path_dir -save path_dir [px]\n"
  python {program_name} path_file path_file -save path_dir [px] *\n"
  python {program_name} path_file path_file -save path_file [px] *\n"

### show:
  python {program_name} path_dir path_dir -show [px]\n"
  python {program_name} path_file path_dir -show [px]\n"
  python {program_name} path_file path_file -show [px] *\n"

## HTTPS:
### save:
  python {program_name} https/address.com/image.img https/address.com/image.img -save path_dir [px] *\n"
  python {program_name} https/address.com/image.img https/address.com/image.img -save path_file [px] *\n"
  python {program_name} https/address.com/image.img path_dir -save path_dir [px]\n"
  python {program_name} https/address.com/image.img path_dir -save path_file [px]\n"
  python {program_name} path_file https/address.com/image.img -save path_dir [px] *\n"
  python {program_name} path_file https/address.com/image.img -save path_file [px] *\n"

### show:
  python {program_name} https/address.com/image.img https/address.com/image.img -show [px] *\n"
  python {program_name} path_file https/address.com/image.img -show [px] *\n"
  python {program_name} https/address.com/image.img path_file -show [px] *\n"
  python {program_name} https/address.com/image.img path_dir -show [px]\n"

* images have to be the same size
