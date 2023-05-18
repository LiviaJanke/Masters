# call by : gawk -v time=12,18,00 -v species=SPEC# -f make_profile.awk SLIMCATname
# 
#

BEGIN {
  printf "# height mixing ratio\n" > "todamf.mod.ref";
  printf "# time=%f species #=%d ",time,species > "todamf.mod.ref";
  Validtime=0;
}

{
  if (NF==9){
   if ($6==time) {Validtime=1;sza=$8;printf("sza=%f\n",sza) > "todamf.mod.ref";}
   else          Validtime=0;
  }

#  print NF,Validtime;
  if (NF==24 && Validtime==1) {
    for(i=1;i<=24;i++) temp[i]=$(25-i);
    getline;
    for(i=1;i<=24;i++) press[i]=$(25-i)/100.;
    getline;
    getline;
    for(i=1;i<=24;i++) h[i]=$(25-i)/1000;
    getline;
    for(i=1;i<species-4;i++) getline;
    for(i=1;i<=24;i++) {
     mixing[i]=$(25-i);
     conc[i]=mixing[i]*7.2427e18*press[i]/temp[i];
     printf "%f %6.4g\n",h[i],conc[i] > "todamf.mod.ref";
    }
    Validtime=0;
  }
 
}
