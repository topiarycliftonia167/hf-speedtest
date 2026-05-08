"""Major airport IATA code → (city, ISO 3166-1 alpha-2 country) lookup.

Used to resolve CloudFront PoP codes (x-amz-cf-pop) to a city/country label.
"""

MAJOR_AIRPORT_IATAS: dict[str, tuple[str, str]] = {
    # USA
    "LAX": ("Los Angeles", "US"),
    "JFK": ("New York", "US"),
    "ORD": ("Chicago", "US"),
    "ATL": ("Atlanta", "US"),
    "DFW": ("Dallas", "US"),
    "DEN": ("Denver", "US"),
    "SFO": ("San Francisco", "US"),
    "SEA": ("Seattle", "US"),
    "MIA": ("Miami", "US"),
    "LAS": ("Las Vegas", "US"),
    "MCO": ("Orlando", "US"),
    "EWR": ("Newark", "US"),
    "CLT": ("Charlotte", "US"),
    "PHX": ("Phoenix", "US"),
    "IAH": ("Houston", "US"),
    "BOS": ("Boston", "US"),
    "MSP": ("Minneapolis", "US"),
    "DTW": ("Detroit", "US"),
    "PHL": ("Philadelphia", "US"),
    "LGA": ("New York", "US"),
    "BWI": ("Baltimore", "US"),
    "SLC": ("Salt Lake City", "US"),
    "IAD": ("Washington D.C.", "US"),
    "DCA": ("Washington D.C.", "US"),
    "SAN": ("San Diego", "US"),
    "TPA": ("Tampa", "US"),
    "HNL": ("Honolulu", "US"),
    # Canada
    "YYZ": ("Toronto", "CA"),
    "YVR": ("Vancouver", "CA"),
    "YUL": ("Montreal", "CA"),
    "YYC": ("Calgary", "CA"),
    "YEG": ("Edmonton", "CA"),
    "YOW": ("Ottawa", "CA"),
    "YWG": ("Winnipeg", "CA"),
    "YHZ": ("Halifax", "CA"),
    # United Kingdom
    "LHR": ("London", "GB"),
    "LGW": ("London", "GB"),
    "STN": ("London", "GB"),
    "LTN": ("London", "GB"),
    "MAN": ("Manchester", "GB"),
    "BHX": ("Birmingham", "GB"),
    "EDI": ("Edinburgh", "GB"),
    "GLA": ("Glasgow", "GB"),
    # France
    "CDG": ("Paris", "FR"),
    "ORY": ("Paris", "FR"),
    "NCE": ("Nice", "FR"),
    "LYS": ("Lyon", "FR"),
    "MRS": ("Marseille", "FR"),
    "TLS": ("Toulouse", "FR"),
    "NTE": ("Nantes", "FR"),
    "BOD": ("Bordeaux", "FR"),
    # Germany
    "FRA": ("Frankfurt", "DE"),
    "MUC": ("Munich", "DE"),
    "BER": ("Berlin", "DE"),
    "DUS": ("Düsseldorf", "DE"),
    "HAM": ("Hamburg", "DE"),
    "CGN": ("Cologne", "DE"),
    "STR": ("Stuttgart", "DE"),
    # China (Mainland)
    "PEK": ("Beijing", "CN"),
    "PKX": ("Beijing", "CN"),
    "PVG": ("Shanghai", "CN"),
    "SHA": ("Shanghai", "CN"),
    "CAN": ("Guangzhou", "CN"),
    "CTU": ("Chengdu", "CN"),
    "TFU": ("Chengdu", "CN"),
    "SZX": ("Shenzhen", "CN"),
    "CKG": ("Chongqing", "CN"),
    "WUH": ("Wuhan", "CN"),
    "XIY": ("Xi'an", "CN"),
    "HGH": ("Hangzhou", "CN"),
    # India
    "DEL": ("Delhi", "IN"),
    "BOM": ("Mumbai", "IN"),
    "BLR": ("Bengaluru", "IN"),
    "MAA": ("Chennai", "IN"),
    "CCU": ("Kolkata", "IN"),
    "HYD": ("Hyderabad", "IN"),
    # Brazil
    "GRU": ("Sao Paulo", "BR"),
    "GIG": ("Rio de Janeiro", "BR"),
    "BSB": ("Brasilia", "BR"),
    "CNF": ("Belo Horizonte", "BR"),
    "SSA": ("Salvador", "BR"),
    "FOR": ("Fortaleza", "BR"),
    "POA": ("Porto Alegre", "BR"),
    "REC": ("Recife", "BR"),
    "CWB": ("Curitiba", "BR"),
    # Australia
    "SYD": ("Sydney", "AU"),
    "MEL": ("Melbourne", "AU"),
    "BNE": ("Brisbane", "AU"),
    "PER": ("Perth", "AU"),
    "ADL": ("Adelaide", "AU"),
    "CBR": ("Canberra", "AU"),
    # Japan
    "NRT": ("Tokyo", "JP"),
    "HND": ("Tokyo", "JP"),
    "KIX": ("Osaka", "JP"),
    "ITM": ("Osaka", "JP"),
    "CTS": ("Sapporo", "JP"),
    "FUK": ("Fukuoka", "JP"),
    "OKA": ("Okinawa", "JP"),
    "NGO": ("Nagoya", "JP"),
    # South Africa
    "JNB": ("Johannesburg", "ZA"),
    "CPT": ("Cape Town", "ZA"),
    "DUR": ("Durban", "ZA"),
    # Netherlands
    "AMS": ("Amsterdam", "NL"),
    # Spain
    "MAD": ("Madrid", "ES"),
    "BCN": ("Barcelona", "ES"),
    "PMI": ("Palma de Mallorca", "ES"),
    "AGP": ("Malaga", "ES"),
    "VLC": ("Valencia", "ES"),
    # Italy
    "FCO": ("Rome", "IT"),
    "MXP": ("Milan", "IT"),
    "LIN": ("Milan", "IT"),
    "BLQ": ("Bologna", "IT"),
    "NAP": ("Naples", "IT"),
    "VCE": ("Venice", "IT"),
    "PSA": ("Pisa", "IT"),
    # Russia
    "SVO": ("Moscow", "RU"),
    "DME": ("Moscow", "RU"),
    "VKO": ("Moscow", "RU"),
    "LED": ("Saint Petersburg", "RU"),
    "AER": ("Sochi", "RU"),
    # United Arab Emirates
    "DXB": ("Dubai", "AE"),
    "AUH": ("Abu Dhabi", "AE"),
    # Singapore
    "SIN": ("Singapore", "SG"),
    # Hong Kong
    "HKG": ("Hong Kong", "HK"),
    # South Korea
    "ICN": ("Seoul", "KR"),
    "GMP": ("Seoul", "KR"),
    "CJU": ("Jeju", "KR"),
    # Turkey
    "IST": ("Istanbul", "TR"),
    "SAW": ("Istanbul", "TR"),
    "AYT": ("Antalya", "TR"),
    "ESB": ("Ankara", "TR"),
    "ADB": ("Izmir", "TR"),
    # Switzerland
    "ZRH": ("Zurich", "CH"),
    "GVA": ("Geneva", "CH"),
    # Argentina
    "EZE": ("Buenos Aires", "AR"),
    "AEP": ("Buenos Aires", "AR"),
    # Mexico
    "MEX": ("Mexico City", "MX"),
    "CUN": ("Cancun", "MX"),
    "GDL": ("Guadalajara", "MX"),
    "MTY": ("Monterrey", "MX"),
    # Thailand
    "BKK": ("Bangkok", "TH"),
    "DMK": ("Bangkok", "TH"),
    "HKT": ("Phuket", "TH"),
    "CNX": ("Chiang Mai", "TH"),
    # Malaysia
    "KUL": ("Kuala Lumpur", "MY"),
    # Ireland
    "DUB": ("Dublin", "IE"),
    "SNN": ("Shannon", "IE"),
    # Portugal
    "LIS": ("Lisbon", "PT"),
    "OPO": ("Porto", "PT"),
    "FAO": ("Faro", "PT"),
    # New Zealand
    "AKL": ("Auckland", "NZ"),
    "CHC": ("Christchurch", "NZ"),
    "WLG": ("Wellington", "NZ"),
    # Qatar
    "DOH": ("Doha", "QA"),
    # Saudi Arabia
    "JED": ("Jeddah", "SA"),
    "RUH": ("Riyadh", "SA"),
    "DMM": ("Dammam", "SA"),
    # Egypt
    "CAI": ("Cairo", "EG"),
    # Nigeria
    "LOS": ("Lagos", "NG"),
    "ABV": ("Abuja", "NG"),
    # Kenya
    "NBO": ("Nairobi", "KE"),
    # Ethiopia
    "ADD": ("Addis Ababa", "ET"),
    # Colombia
    "BOG": ("Bogota", "CO"),
    "MDE": ("Medellin", "CO"),
    # Chile
    "SCL": ("Santiago", "CL"),
    # Peru
    "LIM": ("Lima", "PE"),
    # Austria
    "VIE": ("Vienna", "AT"),
    # Belgium
    "BRU": ("Brussels", "BE"),
    # Czech Republic
    "PRG": ("Prague", "CZ"),
    # Denmark
    "CPH": ("Copenhagen", "DK"),
    # Finland
    "HEL": ("Helsinki", "FI"),
    # Greece
    "ATH": ("Athens", "GR"),
    # Hungary
    "BUD": ("Budapest", "HU"),
    # Norway
    "OSL": ("Oslo", "NO"),
    # Poland
    "WAW": ("Warsaw", "PL"),
    "KRK": ("Krakow", "PL"),
    # Sweden
    "ARN": ("Stockholm", "SE"),
}
