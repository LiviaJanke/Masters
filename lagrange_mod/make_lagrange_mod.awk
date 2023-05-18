# call by : gawk -v szamin=80 -v szamax=95 -v SPECIES=7 -v timemin=333300 -v timemax=419700
#                -f make_damf_input_lagrange.awk lagrange_prof_jokionen.txt
BEGIN {
    getline;
    time0=$1;
}
(!/^#/&&NF){
    time = $1;
    sza = $2;
    temp = $3;
    press = $4;
    species = $SPECIES;
    if ( szamin <= sza && sza <= szamax && timemin <= time && time <= timemax ) {
	printf "%3.3f %4.3f %10.6g\n",sza,press,species > "lagrange_modell.txt";
    }
}
