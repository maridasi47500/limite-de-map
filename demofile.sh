
mkdir templates 
python3 scaffold.py user username email password phone country_id:references
python3 scaffold.py country name
python3 scaffold.py city country_id:references name
python3 scaffold.py uservisitcountry user_id country_id:references decouverte_coin_monde photo:file
python3 scaffold.py debutlimitmap lat lon
python3 scaffold.py finlimitdemap lat lon
python3 scaffold.py boundingbox debutlimitmap_id finlimitdemap_id user_id:references
python3 scaffold.py limitdemaphasmusic  boundingbox_id artist title
python3 scaffold.py boundingboxhaslimitsound boundingboxid sound souvenir_description
python3 scaffold.py boudingboxhassouvenir video:file user_id:references boundingbox_id description
