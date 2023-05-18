# Ungewichtetes Interpolieren der Mixing Ratios ueber die Hoehe
#
BEGIN {
  
}

{
  if (NF==9) {
    year=$1;
    month=$2;
    day=$3;
    lat=$4;
    lon=$5;
    hour=$6;
    unkn=$7;
    sza=$8;
    levls=$9
    if (sza<oldsza) sza=-sza;
    szahelp=sqrt(sza*sza);
    oldsza=$8;
    row_count=0;
  }
if (szahelp>=lowerSZA && szahelp <=upperSZA){
  
# ------ extract temperature from current level
  if (row_count==1) {
    for (i=1;i<=24;i++) {
      T[i]=$i;
      printf ("%.4g ",T[i]) >"temperature.txt";
    }
    printf("\n")>"temperature.txt";
  }
  
# ------ extract pressure from current level
  if (row_count==2) {
    for (i=1;i<=24;i++) {
      p[i]=$i/100.;
      lp[i]=log($(i)/100.);
      printf ("%.4g ",p[i]) >"pressure.txt";
    }
    printf("\n")>"pressure.txt";
  }

# ------ extract height from current level
  if (row_count==4) {
    for (i=1;i<=24;i++) {
      h[i]=$i/1000;
      printf ("%.4g ",h[i]) >"height.txt";
    }
    printf("\n")>"height.txt";
  }

# ------ extract concentration from current level
  if (row_count==getrow) {
    
    for(i=1;i<=24;i++){
       yi=$(25-i)*7.2427e18*(p[25-i]/T[25-i]);
       printf "%.4g %4.4g %4.4g \n",szahelp,h[25-i],yi > "todamf.mod";
    }
   } 
  row_count++;
}
}
