#  call by: gawk -f concat_all.awk Slimcat_data.txt > ttt.txt


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
     if ( abendflag == 1 ){
      if ( sza > szaold ) {
       if (NF!=9 && NF!=24) {
   	  l1=$0; getline;
          l2=$0; getline;
          l3=$0; getline;
          print l1, l2, l3, $0;
       } else {
        print $0;
        }
       }
      } else {
      if ( sza < szaold ) {
       if (NF!=9 && NF!=20) {
          l1=$0; getline;
          l2=$0; getline;
          l3=$0; getline;
          print l1, l2, l3, $0;
       } else {
        print $0;
       }
      }
     }
    }
}
