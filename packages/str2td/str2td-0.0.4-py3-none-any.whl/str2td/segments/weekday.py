# fmt: off
WEEKDAYS = [
	'mo',           'tu',      'we',        'th',       'fr',     'sa',       'su',
	'mon',          'tue',     'wed',       'thu',      'fri',    'sat',      'sun',
	'monday',       'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',

	"po",           "wt",      "sr",        "cz",       "pi",     "so",       "ni",
	"pn",           "wt",      "śr",        "cz",       "pt",     "so",       "nd",
	"pon",          "wto",     "śro",       "czw",      "pią",    "sob",      "nie",
	"pon",          "wto",     "sro",       "czw",      "pia",    "sob",      "nie",
	"poniedzialek", "wtorek",  "sroda",     "czwartek", "piatek", "sobota",   "niedziela",
	"poniedziałek", "wtorek",  "środa",     "czwartek", "piątek", "sobota",   "niedziela",
]
# fmt: on

if any(not s.lower() for s in WEEKDAYS):
	raise RuntimeError("all WEEKDAYS must be lowercase, since they're lowered to case-insensitively compare when evaluating.")
