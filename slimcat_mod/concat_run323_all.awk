# call by : gawk -v time=12,18,00 -v species=SPEC# -f make_profile.awk SLIMCATname
# 
#
BEGIN{
    getline; getline; getline;
    for(i=1;i<167;i++) getline;
    first_block = 1;
    getline; getline; getline;
    if ( NF == 9 ) sza = $8;
}
{    
    if ( $1 == "SLIMCAT" ) {
	getline;
        getline;
        getline;
        if ( NF == 9 ) { szaold=sza; sza = $8;}
	first_block = 0;
    }
    if ( first_block == 0 ){
     
       if (NF!=9 && NF!=24) {
   	  l1=$0; getline;
          l2=$0; getline;
          l3=$0; getline;
          print l1, l2, l3, $0;
       } else {
        print $0;}
    }
}
