import { useState, useEffect, useRef, useMemo, useCallback } from "react";
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts";
import * as d3 from "d3";

const D = {"seasons":[{"n":1,"name":"Borneo","era":"classic","winner":"Richard Hatch","vote":"4-3","cast":16,"days":39,"prize":1000000,"mechs":0,"loc":"Pulau Tiga, Malaysia","avgV":26.4},{"n":2,"name":"The Australian Outback","era":"classic","winner":"Tina Wesson","vote":"4-3","cast":16,"days":42,"prize":1000000,"mechs":0,"loc":"Queensland, Australia","avgV":29.8},{"n":3,"name":"Africa","era":"classic","winner":"Ethan Zohn","vote":"5-2","cast":16,"days":39,"prize":1000000,"mechs":0,"loc":"Shaba Reserve, Kenya","avgV":16.8},{"n":4,"name":"Marquesas","era":"classic","winner":"Vecepia Towery","vote":"4-3","cast":16,"days":39,"prize":1000000,"mechs":0,"loc":"Nuku Hiva, French Polynesia","avgV":17.4},{"n":5,"name":"Thailand","era":"classic","winner":"Brian Heidik","vote":"4-3","cast":16,"days":39,"prize":1000000,"mechs":0,"loc":"Ko Tarutao, Thailand","avgV":15.1},{"n":6,"name":"The Amazon","era":"classic","winner":"Jenna Morasca","vote":"6-1","cast":16,"days":39,"prize":1000000,"mechs":0,"loc":"Rio Negro, Brazil","avgV":14.2},{"n":7,"name":"Pearl Islands","era":"classic","winner":"Sandra Diaz-Twine","vote":"6-1","cast":16,"days":39,"prize":1000000,"mechs":0,"loc":"Panama","avgV":21.1},{"n":8,"name":"All-Stars","era":"classic","winner":"Amber Brkich","vote":"4-3","cast":18,"days":39,"prize":1000000,"mechs":0,"loc":"Panama","avgV":18.7},{"n":9,"name":"Vanuatu","era":"classic","winner":"Chris Daugherty","vote":"5-2","cast":18,"days":39,"prize":1000000,"mechs":0,"loc":"Efate, Vanuatu","avgV":14.3},{"n":10,"name":"Palau","era":"classic","winner":"Tom Westman","vote":"6-1","cast":20,"days":39,"prize":1000000,"mechs":0,"loc":"Koror, Palau","avgV":16.3},{"n":11,"name":"Guatemala","era":"classic","winner":"Danni Boatwright","vote":"6-1","cast":18,"days":39,"prize":1000000,"mechs":1,"loc":"Yaxha, Guatemala","avgV":13.1},{"n":12,"name":"Panama - Exile Island","era":"classic","winner":"Aras Baskauskas","vote":"5-2","cast":16,"days":39,"prize":1000000,"mechs":2,"loc":"Panama","avgV":12.8},{"n":13,"name":"Cook Islands","era":"classic","winner":"Yul Kwon","vote":"5-4-0","cast":20,"days":39,"prize":1000000,"mechs":2,"loc":"Aitutaki, Cook Islands","avgV":12.1},{"n":14,"name":"Fiji","era":"classic","winner":"Earl Cole","vote":"9-0-0","cast":19,"days":39,"prize":1000000,"mechs":2,"loc":"Vanua Levu, Fiji","avgV":11.8},{"n":15,"name":"China","era":"classic","winner":"Todd Herzog","vote":"4-2-1","cast":16,"days":39,"prize":1000000,"mechs":2,"loc":"Zhelin, Jiujiang, China","avgV":13.1},{"n":16,"name":"Micronesia - Fans vs. Favorites","era":"classic","winner":"Parvati Shallow","vote":"5-3","cast":20,"days":39,"prize":1000000,"mechs":2,"loc":"Palau","avgV":0},{"n":17,"name":"Gabon","era":"classic","winner":"Bob Crowley","vote":"4-3-0","cast":18,"days":39,"prize":1000000,"mechs":2,"loc":"Wonga-Wongue, Gabon","avgV":11.5},{"n":18,"name":"Tocantins","era":"classic","winner":"J.T. Thomas","vote":"7-0","cast":16,"days":39,"prize":1000000,"mechs":2,"loc":"Jalapao, Brazil","avgV":11.2},{"n":19,"name":"Samoa","era":"classic","winner":"Natalie White","vote":"7-2-0","cast":20,"days":39,"prize":1000000,"mechs":2,"loc":"Upolu, Samoa","avgV":11.7},{"n":20,"name":"Heroes vs. Villains","era":"classic","winner":"Sandra Diaz-Twine","vote":"6-3-0","cast":20,"days":39,"prize":1000000,"mechs":2,"loc":"Upolu, Samoa","avgV":17.1},{"n":21,"name":"Nicaragua","era":"modern","winner":"Jud \"Fabio\" Birza","vote":"5-4-0","cast":20,"days":39,"prize":1000000,"mechs":1,"loc":"San Juan del Sur, Nicaragua","avgV":0},{"n":22,"name":"Redemption Island","era":"modern","winner":"Rob Mariano","vote":"8-1-0","cast":18,"days":39,"prize":1000000,"mechs":2,"loc":"Nicaragua","avgV":0},{"n":23,"name":"South Pacific","era":"modern","winner":"Sophie Clarke","vote":"6-3-0","cast":18,"days":39,"prize":1000000,"mechs":2,"loc":"Upolu, Samoa","avgV":0},{"n":24,"name":"One World","era":"modern","winner":"Kim Spradlin","vote":"7-2-0","cast":18,"days":39,"prize":1000000,"mechs":1,"loc":"Upolu, Samoa","avgV":0},{"n":25,"name":"Philippines","era":"modern","winner":"Denise Stapley","vote":"6-1-1","cast":18,"days":39,"prize":1000000,"mechs":1,"loc":"Caramoan, Philippines","avgV":10.4},{"n":26,"name":"Caramoan - Fans vs. Favorites","era":"modern","winner":"John Cochran","vote":"8-0-0","cast":20,"days":39,"prize":1000000,"mechs":1,"loc":"Caramoan, Philippines","avgV":0},{"n":27,"name":"Blood vs. Water","era":"modern","winner":"Tyson Apostol","vote":"7-1-0","cast":20,"days":39,"prize":1000000,"mechs":2,"loc":"Palaui, Philippines","avgV":0},{"n":28,"name":"Cagayan - Brawn vs. Brains vs. Beauty","era":"modern","winner":"Tony Vlachos","vote":"8-1","cast":18,"days":39,"prize":1000000,"mechs":1,"loc":"Cagayan, Philippines","avgV":9.6},{"n":29,"name":"San Juan del Sur - Blood vs. Water","era":"modern","winner":"Natalie Anderson","vote":"5-2-1","cast":18,"days":39,"prize":1000000,"mechs":1,"loc":"Nicaragua","avgV":0},{"n":30,"name":"Worlds Apart","era":"modern","winner":"Mike Holloway","vote":"6-1-1","cast":18,"days":39,"prize":1000000,"mechs":1,"loc":"Nicaragua","avgV":0},{"n":31,"name":"Cambodia - Second Chance","era":"modern","winner":"Jeremy Collins","vote":"10-0-0","cast":20,"days":39,"prize":1000000,"mechs":1,"loc":"Koh Rong, Cambodia","avgV":0},{"n":32,"name":"Kaoh Rong - Brains vs. Brawn vs. Beauty","era":"modern","winner":"Michele Fitzgerald","vote":"5-2-0","cast":18,"days":39,"prize":1000000,"mechs":1,"loc":"Koh Rong, Cambodia","avgV":0},{"n":33,"name":"Millennials vs. Gen X","era":"modern","winner":"Adam Klein","vote":"10-0-0","cast":20,"days":39,"prize":1000000,"mechs":1,"loc":"Mamanuca, Fiji","avgV":0},{"n":34,"name":"Game Changers","era":"modern","winner":"Sarah Lacina","vote":"7-3-0","cast":20,"days":39,"prize":1000000,"mechs":1,"loc":"Mamanuca, Fiji","avgV":0},{"n":35,"name":"Heroes vs. Healers vs. Hustlers","era":"modern","winner":"Ben Driebergen","vote":"5-2-1","cast":18,"days":39,"prize":1000000,"mechs":2,"loc":"Mamanuca, Fiji","avgV":0},{"n":36,"name":"Ghost Island","era":"modern","winner":"Wendell Holland","vote":"5-5-0 tiebreak 6-5-0","cast":20,"days":39,"prize":1000000,"mechs":2,"loc":"Mamanuca, Fiji","avgV":7.4},{"n":37,"name":"David vs. Goliath","era":"modern","winner":"Nick Wilson","vote":"7-3-0","cast":20,"days":39,"prize":1000000,"mechs":2,"loc":"Mamanuca, Fiji","avgV":7.3},{"n":38,"name":"Edge of Extinction","era":"modern","winner":"Chris Underwood","vote":"9-4-0","cast":18,"days":39,"prize":1000000,"mechs":3,"loc":"Mamanuca, Fiji","avgV":6.6},{"n":39,"name":"Island of the Idols","era":"modern","winner":"Tommy Sheehan","vote":"8-2-0","cast":20,"days":39,"prize":1000000,"mechs":2,"loc":"Mamanuca, Fiji","avgV":6.2},{"n":40,"name":"Winners at War","era":"modern","winner":"Tony Vlachos","vote":"12-4-0","cast":20,"days":39,"prize":2000000,"mechs":4,"loc":"Mamanuca, Fiji","avgV":5.8},{"n":41,"name":"(New Era)","era":"new_era","winner":"Erika Casupanan","vote":"7-1-0","cast":18,"days":26,"prize":1000000,"mechs":5,"loc":"Mamanuca, Fiji","avgV":5.7},{"n":42,"name":"(New Era)","era":"new_era","winner":"Maryanne Oketch","vote":"7-1-0","cast":18,"days":26,"prize":1000000,"mechs":4,"loc":"Mamanuca, Fiji","avgV":5.4},{"n":43,"name":"(New Era)","era":"new_era","winner":"Mike Gabler","vote":"7-1-0","cast":18,"days":26,"prize":1000000,"mechs":4,"loc":"Mamanuca, Fiji","avgV":5.0},{"n":44,"name":"(New Era)","era":"new_era","winner":"Yam Yam Arocho","vote":"7-1-0","cast":18,"days":26,"prize":1000000,"mechs":4,"loc":"Mamanuca, Fiji","avgV":5.0},{"n":45,"name":"(New Era)","era":"new_era","winner":"Dee Valladares","vote":"5-3-0","cast":18,"days":26,"prize":1000000,"mechs":4,"loc":"Mamanuca, Fiji","avgV":5.0},{"n":46,"name":"(New Era)","era":"new_era","winner":"Kenzie Petty","vote":"5-3-0","cast":18,"days":26,"prize":1000000,"mechs":4,"loc":"Mamanuca, Fiji","avgV":4.7},{"n":47,"name":"(New Era)","era":"new_era","winner":"Rachel LaMont","vote":"7-1-0","cast":18,"days":26,"prize":1000000,"mechs":4,"loc":"Mamanuca, Fiji","avgV":4.4},{"n":48,"name":"(New Era)","era":"new_era","winner":"Kyle Fraser","vote":"5-2-1","cast":18,"days":26,"prize":1000000,"mechs":4,"loc":"Mamanuca, Fiji","avgV":4.6},{"n":49,"name":"(New Era)","era":"new_era","winner":"Savannah Louie","vote":"5-2-1","cast":18,"days":26,"prize":1000000,"mechs":4,"loc":"Mamanuca, Fiji","avgV":4.3},{"n":50,"name":"In the Hands of the Fans","era":"new_era","winner":"Jonathan Young","vote":"TBA","cast":24,"days":26,"prize":2000000,"mechs":4,"loc":"Mamanuca, Fiji","avgV":5.0}],"returners":[{"name":"Rob Mariano","tp":5,"ss":[4,8,20,22,40]},{"name":"Sandra Diaz-Twine","tp":4,"ss":[7,20,34,40]},{"name":"Cirie Fields","tp":4,"ss":[12,16,20,34]},{"name":"Parvati Shallow","tp":4,"ss":[13,16,20,40]},{"name":"Tyson Apostol","tp":4,"ss":[18,20,27,40]},{"name":"Jeff Varner","tp":3,"ss":[2,31,34]},{"name":"Jerri Manthey","tp":3,"ss":[2,8,20]},{"name":"Colby Donaldson","tp":3,"ss":[2,8,20]},{"name":"Tina Wesson","tp":3,"ss":[2,8,27]},{"name":"Ethan Zohn","tp":3,"ss":[3,8,40]},{"name":"Rupert Boneham","tp":3,"ss":[7,8,20]},{"name":"Stephenie LaGrossa","tp":3,"ss":[10,11,20]},{"name":"Jonathan Penner","tp":3,"ss":[13,16,25]},{"name":"Ozzy Lusth","tp":3,"ss":[13,16,34]},{"name":"James Clement","tp":3,"ss":[15,16,20]},{"name":"Amanda Kimmel","tp":3,"ss":[15,16,20]},{"name":"Coach Wade","tp":3,"ss":[18,20,23]},{"name":"J.T. Thomas","tp":3,"ss":[18,20,34]},{"name":"Russell Hantz","tp":3,"ss":[19,20,22]},{"name":"Andrea Boehlke","tp":3,"ss":[22,26,34]},{"name":"Malcolm Freberg","tp":3,"ss":[25,26,34]},{"name":"Ciera Eastin","tp":3,"ss":[27,31,34]},{"name":"Sarah Lacina","tp":3,"ss":[28,34,40]},{"name":"Tony Vlachos","tp":3,"ss":[28,34,40]},{"name":"Kelley Wentworth","tp":3,"ss":[29,31,38]}],"quality":{"total":699,"title":692,"date":698,"tc":648,"chal":188,"view":486,"detailed":642,"notable":324,"season-level":56,"stub":1},"eras":{"classic":20,"modern":20,"new_era":10},"elimMethods":{"vote":663,"medevac":18,"rock_draw":4,"quit":8,"ejection":4,"fire_making":8,"default":1},"challengeTypes":{"immunity":188,"reward":33},"eraViewership":{"classic":{"avg":15.8,"min":10.7,"max":51.7,"n":266},"modern":{"avg":7.6,"min":4.3,"max":11.5,"n":98},"new_era":{"avg":4.9,"min":3.9,"max":6.2,"n":122}},"graph":{"n":[{"id":"season-1","t":"S","l":"S1: Borneo","era":"classic","w":"Richard Hatch","v":"4-3","c":16,"loc":"Pulau Tiga, Malaysia"},{"id":"season-2","t":"S","l":"S2: The Australian Outback","era":"classic","w":"Tina Wesson","v":"4-3","c":16,"loc":"Queensland, Australia"},{"id":"season-3","t":"S","l":"S3: Africa","era":"classic","w":"Ethan Zohn","v":"5-2","c":16,"loc":"Shaba Reserve, Kenya"},{"id":"season-4","t":"S","l":"S4: Marquesas","era":"classic","w":"Vecepia Towery","v":"4-3","c":16,"loc":"Nuku Hiva, French Polynesia"},{"id":"season-5","t":"S","l":"S5: Thailand","era":"classic","w":"Brian Heidik","v":"4-3","c":16,"loc":"Ko Tarutao, Thailand"},{"id":"season-6","t":"S","l":"S6: The Amazon","era":"classic","w":"Jenna Morasca","v":"6-1","c":16,"loc":"Rio Negro, Brazil"},{"id":"season-7","t":"S","l":"S7: Pearl Islands","era":"classic","w":"Sandra Diaz-Twine","v":"6-1","c":16,"loc":"Panama"},{"id":"season-8","t":"S","l":"S8: All-Stars","era":"classic","w":"Amber Brkich","v":"4-3","c":18,"loc":"Panama"},{"id":"season-9","t":"S","l":"S9: Vanuatu","era":"classic","w":"Chris Daugherty","v":"5-2","c":18,"loc":"Efate, Vanuatu"},{"id":"season-10","t":"S","l":"S10: Palau","era":"classic","w":"Tom Westman","v":"6-1","c":20,"loc":"Koror, Palau"},{"id":"season-11","t":"S","l":"S11: Guatemala","era":"classic","w":"Danni Boatwright","v":"6-1","c":18,"loc":"Yaxha, Guatemala"},{"id":"season-12","t":"S","l":"S12: Panama - Exile Island","era":"classic","w":"Aras Baskauskas","v":"5-2","c":16,"loc":"Panama"},{"id":"season-13","t":"S","l":"S13: Cook Islands","era":"classic","w":"Yul Kwon","v":"5-4-0","c":20,"loc":"Aitutaki, Cook Islands"},{"id":"season-14","t":"S","l":"S14: Fiji","era":"classic","w":"Earl Cole","v":"9-0-0","c":19,"loc":"Vanua Levu, Fiji"},{"id":"season-15","t":"S","l":"S15: China","era":"classic","w":"Todd Herzog","v":"4-2-1","c":16,"loc":"Zhelin, Jiujiang, China"},{"id":"season-16","t":"S","l":"S16: Micronesia - Fans vs. Favorites","era":"classic","w":"Parvati Shallow","v":"5-3","c":20,"loc":"Palau"},{"id":"season-17","t":"S","l":"S17: Gabon","era":"classic","w":"Bob Crowley","v":"4-3-0","c":18,"loc":"Wonga-Wongue, Gabon"},{"id":"season-18","t":"S","l":"S18: Tocantins","era":"classic","w":"J.T. Thomas","v":"7-0","c":16,"loc":"Jalapao, Brazil"},{"id":"season-19","t":"S","l":"S19: Samoa","era":"classic","w":"Natalie White","v":"7-2-0","c":20,"loc":"Upolu, Samoa"},{"id":"season-20","t":"S","l":"S20: Heroes vs. Villains","era":"classic","w":"Sandra Diaz-Twine","v":"6-3-0","c":20,"loc":"Upolu, Samoa"},{"id":"season-21","t":"S","l":"S21: Nicaragua","era":"modern","w":"Jud \"Fabio\" Birza","v":"5-4-0","c":20,"loc":"San Juan del Sur, Nicaragua"},{"id":"season-22","t":"S","l":"S22: Redemption Island","era":"modern","w":"Rob Mariano","v":"8-1-0","c":18,"loc":"Nicaragua"},{"id":"season-23","t":"S","l":"S23: South Pacific","era":"modern","w":"Sophie Clarke","v":"6-3-0","c":18,"loc":"Upolu, Samoa"},{"id":"season-24","t":"S","l":"S24: One World","era":"modern","w":"Kim Spradlin","v":"7-2-0","c":18,"loc":"Upolu, Samoa"},{"id":"season-25","t":"S","l":"S25: Philippines","era":"modern","w":"Denise Stapley","v":"6-1-1","c":18,"loc":"Caramoan, Philippines"},{"id":"season-26","t":"S","l":"S26: Caramoan - Fans vs. Favorites","era":"modern","w":"John Cochran","v":"8-0-0","c":20,"loc":"Caramoan, Philippines"},{"id":"season-27","t":"S","l":"S27: Blood vs. Water","era":"modern","w":"Tyson Apostol","v":"7-1-0","c":20,"loc":"Palaui, Philippines"},{"id":"season-28","t":"S","l":"S28: Cagayan - Brawn vs. Brains vs. Beauty","era":"modern","w":"Tony Vlachos","v":"8-1","c":18,"loc":"Cagayan, Philippines"},{"id":"season-29","t":"S","l":"S29: San Juan del Sur - Blood vs. Water","era":"modern","w":"Natalie Anderson","v":"5-2-1","c":18,"loc":"Nicaragua"},{"id":"season-30","t":"S","l":"S30: Worlds Apart","era":"modern","w":"Mike Holloway","v":"6-1-1","c":18,"loc":"Nicaragua"},{"id":"season-31","t":"S","l":"S31: Cambodia - Second Chance","era":"modern","w":"Jeremy Collins","v":"10-0-0","c":20,"loc":"Koh Rong, Cambodia"},{"id":"season-32","t":"S","l":"S32: Kaoh Rong - Brains vs. Brawn vs. Beauty","era":"modern","w":"Michele Fitzgerald","v":"5-2-0","c":18,"loc":"Koh Rong, Cambodia"},{"id":"season-33","t":"S","l":"S33: Millennials vs. Gen X","era":"modern","w":"Adam Klein","v":"10-0-0","c":20,"loc":"Mamanuca, Fiji"},{"id":"season-34","t":"S","l":"S34: Game Changers","era":"modern","w":"Sarah Lacina","v":"7-3-0","c":20,"loc":"Mamanuca, Fiji"},{"id":"season-35","t":"S","l":"S35: Heroes vs. Healers vs. Hustlers","era":"modern","w":"Ben Driebergen","v":"5-2-1","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-36","t":"S","l":"S36: Ghost Island","era":"modern","w":"Wendell Holland","v":"5-5-0 tiebreak 6-5-0","c":20,"loc":"Mamanuca, Fiji"},{"id":"season-37","t":"S","l":"S37: David vs. Goliath","era":"modern","w":"Nick Wilson","v":"7-3-0","c":20,"loc":"Mamanuca, Fiji"},{"id":"season-38","t":"S","l":"S38: Edge of Extinction","era":"modern","w":"Chris Underwood","v":"9-4-0","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-39","t":"S","l":"S39: Island of the Idols","era":"modern","w":"Tommy Sheehan","v":"8-2-0","c":20,"loc":"Mamanuca, Fiji"},{"id":"season-40","t":"S","l":"S40: Winners at War","era":"modern","w":"Tony Vlachos","v":"12-4-0","c":20,"loc":"Mamanuca, Fiji"},{"id":"season-41","t":"S","l":"S41: (New Era)","era":"new_era","w":"Erika Casupanan","v":"7-1-0","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-42","t":"S","l":"S42: (New Era)","era":"new_era","w":"Maryanne Oketch","v":"7-1-0","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-43","t":"S","l":"S43: (New Era)","era":"new_era","w":"Mike Gabler","v":"7-1-0","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-44","t":"S","l":"S44: (New Era)","era":"new_era","w":"Yam Yam Arocho","v":"7-1-0","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-45","t":"S","l":"S45: (New Era)","era":"new_era","w":"Dee Valladares","v":"5-3-0","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-46","t":"S","l":"S46: (New Era)","era":"new_era","w":"Kenzie Petty","v":"5-3-0","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-47","t":"S","l":"S47: (New Era)","era":"new_era","w":"Rachel LaMont","v":"7-1-0","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-48","t":"S","l":"S48: (New Era)","era":"new_era","w":"Kyle Fraser","v":"5-2-1","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-49","t":"S","l":"S49: (New Era)","era":"new_era","w":"Savannah Louie","v":"5-2-1","c":18,"loc":"Mamanuca, Fiji"},{"id":"season-50","t":"S","l":"S50: In the Hands of the Fans","era":"new_era","w":"Jonathan Young","v":"TBA","c":24,"loc":"Mamanuca, Fiji"},{"id":"person-jenna-lewis","t":"P","l":"Jenna Lewis","tp":2,"ss":[1,8]},{"id":"person-gervase-peterson","t":"P","l":"Gervase Peterson","tp":2,"ss":[1,27]},{"id":"person-rudy-boesch","t":"P","l":"Rudy Boesch","tp":2,"ss":[1,8]},{"id":"person-kelly-wiglesworth","t":"P","l":"Kelly Wiglesworth","tp":2,"ss":[1,31]},{"id":"person-richard-hatch","t":"P","l":"Richard Hatch","tp":2,"ss":[1,8]},{"id":"person-kimmi-kappenberg","t":"P","l":"Kimmi Kappenberg","tp":2,"ss":[2,31]},{"id":"person-michael-skupin","t":"P","l":"Michael Skupin","tp":2,"ss":[2,25]},{"id":"person-jeff-varner","t":"P","l":"Jeff Varner","tp":3,"ss":[2,31,34]},{"id":"person-alicia-calaway","t":"P","l":"Alicia Calaway","tp":2,"ss":[2,8]},{"id":"person-jerri-manthey","t":"P","l":"Jerri Manthey","tp":3,"ss":[2,8,20]},{"id":"person-amber-brkich","t":"P","l":"Amber Brkich","tp":2,"ss":[2,8]},{"id":"person-colby-donaldson","t":"P","l":"Colby Donaldson","tp":3,"ss":[2,8,20]},{"id":"person-tina-wesson","t":"P","l":"Tina Wesson","tp":3,"ss":[2,8,27]},{"id":"person-lex-van-den-berghe","t":"P","l":"Lex van den Berghe","tp":2,"ss":[3,8]},{"id":"person-tom-buchanan","t":"P","l":"Tom Buchanan","tp":2,"ss":[3,8]},{"id":"person-ethan-zohn","t":"P","l":"Ethan Zohn","tp":3,"ss":[3,8,40]},{"id":"person-rob-mariano","t":"P","l":"Rob Mariano","tp":5,"ss":[4,8,20,22,40]},{"id":"person-kathy-vavrick-o-brien","t":"P","l":"Kathy Vavrick-O'Brien","tp":2,"ss":[4,8]},{"id":"person-shii-ann-huang","t":"P","l":"Shii Ann Huang","tp":2,"ss":[5,8]},{"id":"person-jenna-morasca","t":"P","l":"Jenna Morasca","tp":2,"ss":[6,8]},{"id":"person-lillian-morris","t":"P","l":"Lillian Morris","tp":2,"ss":[7,7]},{"id":"person-andrew-savage","t":"P","l":"Andrew Savage","tp":2,"ss":[7,31]},{"id":"person-rupert-boneham","t":"P","l":"Rupert Boneham","tp":3,"ss":[7,8,20]},{"id":"person-sandra-diaz-twine","t":"P","l":"Sandra Diaz-Twine","tp":4,"ss":[7,20,34,40]},{"id":"person-ami-cusack","t":"P","l":"Ami Cusack","tp":2,"ss":[9,16]},{"id":"person-eliza-orlins","t":"P","l":"Eliza Orlins","tp":2,"ss":[9,16]},{"id":"person-bobby-jon-drinkard","t":"P","l":"Bobby Jon Drinkard","tp":2,"ss":[10,11]},{"id":"person-stephenie-lagrossa","t":"P","l":"Stephenie LaGrossa","tp":3,"ss":[10,11,20]},{"id":"person-tom-westman","t":"P","l":"Tom Westman","tp":2,"ss":[10,20]},{"id":"person-danni-boatwright","t":"P","l":"Danni Boatwright","tp":2,"ss":[11,40]},{"id":"person-cirie-fields","t":"P","l":"Cirie Fields","tp":4,"ss":[12,16,20,34]},{"id":"person-terry-deitz","t":"P","l":"Terry Deitz","tp":2,"ss":[12,31]},{"id":"person-danielle-dilorenzo","t":"P","l":"Danielle DiLorenzo","tp":2,"ss":[12,20]},{"id":"person-aras-baskauskas","t":"P","l":"Aras Baskauskas","tp":2,"ss":[12,27]},{"id":"person-candice-woodcock","t":"P","l":"Candice Woodcock","tp":2,"ss":[13,20]},{"id":"person-jonathan-penner","t":"P","l":"Jonathan Penner","tp":3,"ss":[13,16,25]},{"id":"person-parvati-shallow","t":"P","l":"Parvati Shallow","tp":4,"ss":[13,16,20,40]},{"id":"person-ozzy-lusth","t":"P","l":"Ozzy Lusth","tp":3,"ss":[13,16,34]},{"id":"person-yul-kwon","t":"P","l":"Yul Kwon","tp":2,"ss":[13,40]},{"id":"person-yau-man-chan","t":"P","l":"Yau-Man Chan","tp":2,"ss":[14,16]},{"id":"person-james-clement","t":"P","l":"James Clement","tp":3,"ss":[15,16,20]},{"id":"person-peih-gee-law","t":"P","l":"Peih-Gee Law","tp":2,"ss":[15,31]},{"id":"person-courtney-yates","t":"P","l":"Courtney Yates","tp":2,"ss":[15,20]},{"id":"person-amanda-kimmel","t":"P","l":"Amanda Kimmel","tp":3,"ss":[15,16,20]},{"id":"person-erik-reichenbach","t":"P","l":"Erik Reichenbach","tp":2,"ss":[16,26]},{"id":"person-randy-bailey","t":"P","l":"Randy Bailey","tp":2,"ss":[17,20]},{"id":"person-corinne-kaplan","t":"P","l":"Corinne Kaplan","tp":2,"ss":[17,26]},{"id":"person-sugar-kiper","t":"P","l":"Sugar Kiper","tp":2,"ss":[17,20]},{"id":"person-tyson-apostol","t":"P","l":"Tyson Apostol","tp":4,"ss":[18,20,27,40]},{"id":"person-coach-wade","t":"P","l":"Coach Wade","tp":3,"ss":[18,20,23]},{"id":"person-stephen-fishbach","t":"P","l":"Stephen Fishbach","tp":2,"ss":[18,31]},{"id":"person-j-t-thomas","t":"P","l":"J.T. Thomas","tp":3,"ss":[18,20,34]},{"id":"person-russell-swan","t":"P","l":"Russell Swan","tp":2,"ss":[19,25]},{"id":"person-laura-morett","t":"P","l":"Laura Morett","tp":2,"ss":[19,27]},{"id":"person-monica-padilla","t":"P","l":"Monica Padilla","tp":2,"ss":[19,31]},{"id":"person-russell-hantz","t":"P","l":"Russell Hantz","tp":3,"ss":[19,20,22]},{"id":"person-brenda-lowe","t":"P","l":"Brenda Lowe","tp":2,"ss":[21,26]},{"id":"person-francesca-hogi","t":"P","l":"Francesca Hogi","tp":2,"ss":[22,26]},{"id":"person-matt-elrod","t":"P","l":"Matt Elrod","tp":2,"ss":[22,22]},{"id":"person-andrea-boehlke","t":"P","l":"Andrea Boehlke","tp":3,"ss":[22,26,34]},{"id":"person-phillip-sheppard","t":"P","l":"Phillip Sheppard","tp":2,"ss":[22,26]},{"id":"person-christine-shields-markoski","t":"P","l":"Christine Shields Markoski","tp":2,"ss":[23,23]},{"id":"person-rick-nelson","t":"P","l":"Rick Nelson","tp":2,"ss":[23,23]},{"id":"person-dawn-meehan","t":"P","l":"Dawn Meehan","tp":2,"ss":[23,26]},{"id":"person-brandon-hantz","t":"P","l":"Brandon Hantz","tp":2,"ss":[23,26]},{"id":"person-sophie-clarke","t":"P","l":"Sophie Clarke","tp":2,"ss":[23,40]},{"id":"person-monica-culpepper","t":"P","l":"Monica Culpepper","tp":2,"ss":[24,27]},{"id":"person-troyzan-robertson","t":"P","l":"Troyzan Robertson","tp":2,"ss":[24,34]},{"id":"person-kat-edorsson","t":"P","l":"Kat Edorsson","tp":2,"ss":[24,27]},{"id":"person-abi-maria-gomes","t":"P","l":"Abi-Maria Gomes","tp":2,"ss":[25,31]},{"id":"person-malcolm-freberg","t":"P","l":"Malcolm Freberg","tp":3,"ss":[25,26,34]},{"id":"person-denise-stapley","t":"P","l":"Denise Stapley","tp":2,"ss":[25,40]},{"id":"person-john-cody","t":"P","l":"John Cody","tp":2,"ss":[27,27]},{"id":"person-brad-culpepper","t":"P","l":"Brad Culpepper","tp":2,"ss":[27,34]},{"id":"person-vytas-baskauskas","t":"P","l":"Vytas Baskauskas","tp":2,"ss":[27,31]},{"id":"person-ciera-eastin","t":"P","l":"Ciera Eastin","tp":3,"ss":[27,31,34]},{"id":"person-sarah-lacina","t":"P","l":"Sarah Lacina","tp":3,"ss":[28,34,40]},{"id":"person-tasha-fox","t":"P","l":"Tasha Fox","tp":2,"ss":[28,31]},{"id":"person-spencer-bledsoe","t":"P","l":"Spencer Bledsoe","tp":2,"ss":[28,31]},{"id":"person-kass-mcquillen","t":"P","l":"Kass McQuillen","tp":2,"ss":[28,31]},{"id":"person-tony-vlachos","t":"P","l":"Tony Vlachos","tp":3,"ss":[28,34,40]},{"id":"person-kelley-wentworth","t":"P","l":"Kelley Wentworth","tp":3,"ss":[29,31,38]},{"id":"person-jeremy-collins","t":"P","l":"Jeremy Collins","tp":3,"ss":[29,31,40]},{"id":"person-keith-nale","t":"P","l":"Keith Nale","tp":2,"ss":[29,31]},{"id":"person-natalie-anderson","t":"P","l":"Natalie Anderson","tp":2,"ss":[29,40]},{"id":"person-hali-ford","t":"P","l":"Hali Ford","tp":2,"ss":[30,34]},{"id":"person-joe-anglim","t":"P","l":"Joe Anglim","tp":3,"ss":[30,31,38]},{"id":"person-shirin-oskooi","t":"P","l":"Shirin Oskooi","tp":2,"ss":[30,31]},{"id":"person-sierra-dawn-thomas","t":"P","l":"Sierra Dawn Thomas","tp":2,"ss":[30,34]},{"id":"person-caleb-reynolds","t":"P","l":"Caleb Reynolds","tp":2,"ss":[32,34]},{"id":"person-debbie-wanner","t":"P","l":"Debbie Wanner","tp":2,"ss":[32,34]},{"id":"person-tai-trang","t":"P","l":"Tai Trang","tp":2,"ss":[32,34]},{"id":"person-aubry-bracco","t":"P","l":"Aubry Bracco","tp":3,"ss":[32,34,38]},{"id":"person-michele-fitzgerald","t":"P","l":"Michele Fitzgerald","tp":2,"ss":[32,40]},{"id":"person-michaela-bradshaw","t":"P","l":"Michaela Bradshaw","tp":2,"ss":[33,34]},{"id":"person-zeke-smith","t":"P","l":"Zeke Smith","tp":2,"ss":[33,34]},{"id":"person-david-wright","t":"P","l":"David Wright","tp":2,"ss":[33,38]},{"id":"person-adam-klein","t":"P","l":"Adam Klein","tp":2,"ss":[33,40]},{"id":"person-ben-driebergen","t":"P","l":"Ben Driebergen","tp":2,"ss":[35,40]},{"id":"person-wendell-holland","t":"P","l":"Wendell Holland","tp":2,"ss":[36,40]},{"id":"person-nick-wilson","t":"P","l":"Nick Wilson","tp":2,"ss":[37,40]},{"id":"person-chris-underwood","t":"P","l":"Chris Underwood","tp":2,"ss":[38,38]},{"id":"person-rick-devens","t":"P","l":"Rick Devens","tp":2,"ss":[38,38]},{"id":"person-owen-knight","t":"P","l":"Owen Knight","tp":2,"ss":[43,43]},{"id":"person-bruce-perreault","t":"P","l":"Bruce Perreault","tp":2,"ss":[44,45]},{"id":"person-brandon-cottom","t":"P","l":"Brandon Cottom","tp":2,"ss":[44,44]},{"id":"person-teeny-chirichillo","t":"P","l":"Teeny Chirichillo","tp":2,"ss":[47,49]},{"id":"person-rachel-lamont","t":"P","l":"Rachel LaMont","tp":2,"ss":[47,47]}],"e":[{"s":"season-1","t":"season-8","r":"returning_player"},{"s":"season-1","t":"season-27","r":"returning_player"},{"s":"season-1","t":"season-31","r":"returning_player"},{"s":"season-2","t":"season-31","r":"returning_player"},{"s":"season-2","t":"season-25","r":"returning_player"},{"s":"season-31","t":"season-34","r":"returning_player"},{"s":"season-2","t":"season-8","r":"returning_player"},{"s":"season-8","t":"season-20","r":"returning_player"},{"s":"season-8","t":"season-27","r":"returning_player"},{"s":"season-3","t":"season-8","r":"returning_player"},{"s":"season-8","t":"season-40","r":"returning_player"},{"s":"season-4","t":"season-8","r":"returning_player"},{"s":"season-20","t":"season-22","r":"returning_player"},{"s":"season-22","t":"season-40","r":"returning_player"},{"s":"season-5","t":"season-8","r":"returning_player"},{"s":"season-6","t":"season-8","r":"returning_player"},{"s":"season-7","t":"season-7","r":"returning_player"},{"s":"season-7","t":"season-31","r":"returning_player"},{"s":"season-7","t":"season-8","r":"returning_player"},{"s":"season-7","t":"season-20","r":"returning_player"},{"s":"season-20","t":"season-34","r":"returning_player"},{"s":"season-34","t":"season-40","r":"returning_player"},{"s":"season-9","t":"season-16","r":"returning_player"},{"s":"season-10","t":"season-11","r":"returning_player"},{"s":"season-11","t":"season-20","r":"returning_player"},{"s":"season-10","t":"season-20","r":"returning_player"},{"s":"season-11","t":"season-40","r":"returning_player"},{"s":"season-12","t":"season-16","r":"returning_player"},{"s":"season-16","t":"season-20","r":"returning_player"},{"s":"season-12","t":"season-31","r":"returning_player"},{"s":"season-12","t":"season-20","r":"returning_player"},{"s":"season-12","t":"season-27","r":"returning_player"},{"s":"season-13","t":"season-20","r":"returning_player"},{"s":"season-13","t":"season-16","r":"returning_player"},{"s":"season-16","t":"season-25","r":"returning_player"},{"s":"season-20","t":"season-40","r":"returning_player"},{"s":"season-16","t":"season-34","r":"returning_player"},{"s":"season-13","t":"season-40","r":"returning_player"},{"s":"season-14","t":"season-16","r":"returning_player"},{"s":"season-15","t":"season-16","r":"returning_player"},{"s":"season-15","t":"season-31","r":"returning_player"},{"s":"season-15","t":"season-20","r":"returning_player"},{"s":"season-16","t":"season-26","r":"returning_player"},{"s":"season-17","t":"season-20","r":"returning_player"},{"s":"season-17","t":"season-26","r":"returning_player"},{"s":"season-18","t":"season-20","r":"returning_player"},{"s":"season-20","t":"season-27","r":"returning_player"},{"s":"season-27","t":"season-40","r":"returning_player"},{"s":"season-20","t":"season-23","r":"returning_player"},{"s":"season-18","t":"season-31","r":"returning_player"},{"s":"season-19","t":"season-25","r":"returning_player"},{"s":"season-19","t":"season-27","r":"returning_player"},{"s":"season-19","t":"season-31","r":"returning_player"},{"s":"season-19","t":"season-20","r":"returning_player"},{"s":"season-21","t":"season-26","r":"returning_player"},{"s":"season-22","t":"season-26","r":"returning_player"},{"s":"season-22","t":"season-22","r":"returning_player"},{"s":"season-26","t":"season-34","r":"returning_player"},{"s":"season-23","t":"season-23","r":"returning_player"},{"s":"season-23","t":"season-26","r":"returning_player"},{"s":"season-23","t":"season-40","r":"returning_player"},{"s":"season-24","t":"season-27","r":"returning_player"},{"s":"season-24","t":"season-34","r":"returning_player"},{"s":"season-25","t":"season-31","r":"returning_player"},{"s":"season-25","t":"season-26","r":"returning_player"},{"s":"season-25","t":"season-40","r":"returning_player"},{"s":"season-27","t":"season-27","r":"returning_player"},{"s":"season-27","t":"season-34","r":"returning_player"},{"s":"season-27","t":"season-31","r":"returning_player"},{"s":"season-28","t":"season-34","r":"returning_player"},{"s":"season-28","t":"season-31","r":"returning_player"},{"s":"season-29","t":"season-31","r":"returning_player"},{"s":"season-31","t":"season-38","r":"returning_player"},{"s":"season-31","t":"season-40","r":"returning_player"},{"s":"season-29","t":"season-40","r":"returning_player"},{"s":"season-30","t":"season-34","r":"returning_player"},{"s":"season-30","t":"season-31","r":"returning_player"},{"s":"season-32","t":"season-34","r":"returning_player"},{"s":"season-34","t":"season-38","r":"returning_player"},{"s":"season-32","t":"season-40","r":"returning_player"},{"s":"season-33","t":"season-34","r":"returning_player"},{"s":"season-33","t":"season-38","r":"returning_player"},{"s":"season-33","t":"season-40","r":"returning_player"},{"s":"season-35","t":"season-40","r":"returning_player"},{"s":"season-36","t":"season-40","r":"returning_player"},{"s":"season-37","t":"season-40","r":"returning_player"},{"s":"season-38","t":"season-38","r":"returning_player"},{"s":"season-43","t":"season-43","r":"returning_player"},{"s":"season-44","t":"season-45","r":"returning_player"},{"s":"season-44","t":"season-44","r":"returning_player"},{"s":"season-47","t":"season-49","r":"returning_player"},{"s":"season-47","t":"season-47","r":"returning_player"},{"s":"person-jenna-lewis","t":"contestant-jenna-lewis-s1","r":"same_person"},{"s":"person-jenna-lewis","t":"contestant-jenna-lewis-s8","r":"same_person"},{"s":"person-gervase-peterson","t":"contestant-gervase-peterson-s1","r":"same_person"},{"s":"person-gervase-peterson","t":"contestant-gervase-peterson-s27","r":"same_person"},{"s":"person-rudy-boesch","t":"contestant-rudy-boesch-s1","r":"same_person"},{"s":"person-rudy-boesch","t":"contestant-rudy-boesch-s8","r":"same_person"},{"s":"person-kelly-wiglesworth","t":"contestant-kelly-wiglesworth-s1","r":"same_person"},{"s":"person-kelly-wiglesworth","t":"contestant-kelly-wiglesworth-s31","r":"same_person"},{"s":"person-richard-hatch","t":"contestant-richard-hatch-s1","r":"same_person"},{"s":"person-richard-hatch","t":"contestant-richard-hatch-s8","r":"same_person"},{"s":"person-kimmi-kappenberg","t":"contestant-kimmi-kappenberg-s2","r":"same_person"},{"s":"person-kimmi-kappenberg","t":"contestant-kimmi-kappenberg-s31","r":"same_person"},{"s":"person-michael-skupin","t":"contestant-michael-skupin-s2","r":"same_person"},{"s":"person-michael-skupin","t":"contestant-michael-skupin-s25","r":"same_person"},{"s":"person-jeff-varner","t":"contestant-jeff-varner-s2","r":"same_person"},{"s":"person-jeff-varner","t":"contestant-jeff-varner-s31","r":"same_person"},{"s":"person-jeff-varner","t":"contestant-jeff-varner-s34","r":"same_person"},{"s":"person-alicia-calaway","t":"contestant-alicia-calaway-s2","r":"same_person"},{"s":"person-alicia-calaway","t":"contestant-alicia-calaway-s8","r":"same_person"},{"s":"person-jerri-manthey","t":"contestant-jerri-manthey-s2","r":"same_person"},{"s":"person-jerri-manthey","t":"contestant-jerri-manthey-s8","r":"same_person"},{"s":"person-jerri-manthey","t":"contestant-jerri-manthey-s20","r":"same_person"},{"s":"person-amber-brkich","t":"contestant-amber-brkich-s2","r":"same_person"},{"s":"person-amber-brkich","t":"contestant-amber-brkich-s8","r":"same_person"},{"s":"person-colby-donaldson","t":"contestant-colby-donaldson-s2","r":"same_person"},{"s":"person-colby-donaldson","t":"contestant-colby-donaldson-s8","r":"same_person"},{"s":"person-colby-donaldson","t":"contestant-colby-donaldson-s20","r":"same_person"},{"s":"person-tina-wesson","t":"contestant-tina-wesson-s2","r":"same_person"},{"s":"person-tina-wesson","t":"contestant-tina-wesson-s8","r":"same_person"},{"s":"person-tina-wesson","t":"contestant-tina-wesson-s27","r":"same_person"},{"s":"person-lex-van-den-berghe","t":"contestant-lex-van-den-berghe-s3","r":"same_person"},{"s":"person-lex-van-den-berghe","t":"contestant-lex-van-den-berghe-s8","r":"same_person"},{"s":"person-tom-buchanan","t":"contestant-tom-buchanan-s3","r":"same_person"},{"s":"person-tom-buchanan","t":"contestant-tom-buchanan-s8","r":"same_person"},{"s":"person-ethan-zohn","t":"contestant-ethan-zohn-s3","r":"same_person"},{"s":"person-ethan-zohn","t":"contestant-ethan-zohn-s8","r":"same_person"},{"s":"person-ethan-zohn","t":"contestant-ethan-zohn-s40","r":"same_person"},{"s":"person-rob-mariano","t":"contestant-rob-mariano-s4","r":"same_person"},{"s":"person-rob-mariano","t":"contestant-rob-mariano-s8","r":"same_person"},{"s":"person-rob-mariano","t":"contestant-rob-mariano-s20","r":"same_person"},{"s":"person-rob-mariano","t":"contestant-rob-mariano-s22","r":"same_person"},{"s":"person-rob-mariano","t":"contestant-rob-mariano-s40","r":"same_person"},{"s":"person-kathy-vavrick-o-brien","t":"contestant-kathy-vavrick-o-brien-s4","r":"same_person"},{"s":"person-kathy-vavrick-o-brien","t":"contestant-kathy-vavrick-o-brien-s8","r":"same_person"},{"s":"person-shii-ann-huang","t":"contestant-shii-ann-huang-s5","r":"same_person"},{"s":"person-shii-ann-huang","t":"contestant-shii-ann-huang-s8","r":"same_person"},{"s":"person-jenna-morasca","t":"contestant-jenna-morasca-s6","r":"same_person"},{"s":"person-jenna-morasca","t":"contestant-jenna-morasca-s8","r":"same_person"},{"s":"person-lillian-morris","t":"contestant-lillian-morris-s7","r":"same_person"},{"s":"person-lillian-morris","t":"contestant-lillian-morris-s7","r":"same_person"},{"s":"person-andrew-savage","t":"contestant-andrew-savage-s7","r":"same_person"},{"s":"person-andrew-savage","t":"contestant-andrew-savage-s31","r":"same_person"},{"s":"person-rupert-boneham","t":"contestant-rupert-boneham-s7","r":"same_person"},{"s":"person-rupert-boneham","t":"contestant-rupert-boneham-s8","r":"same_person"},{"s":"person-rupert-boneham","t":"contestant-rupert-boneham-s20","r":"same_person"},{"s":"person-sandra-diaz-twine","t":"contestant-sandra-diaz-twine-s7","r":"same_person"},{"s":"person-sandra-diaz-twine","t":"contestant-sandra-diaz-twine-s20","r":"same_person"},{"s":"person-sandra-diaz-twine","t":"contestant-sandra-diaz-twine-s34","r":"same_person"},{"s":"person-sandra-diaz-twine","t":"contestant-sandra-diaz-twine-s40","r":"same_person"},{"s":"person-ami-cusack","t":"contestant-ami-cusack-s9","r":"same_person"},{"s":"person-ami-cusack","t":"contestant-ami-cusack-s16","r":"same_person"},{"s":"person-eliza-orlins","t":"contestant-eliza-orlins-s9","r":"same_person"},{"s":"person-eliza-orlins","t":"contestant-eliza-orlins-s16","r":"same_person"},{"s":"person-bobby-jon-drinkard","t":"contestant-bobby-jon-drinkard-s10","r":"same_person"},{"s":"person-bobby-jon-drinkard","t":"contestant-bobby-jon-drinkard-s11","r":"same_person"},{"s":"person-stephenie-lagrossa","t":"contestant-stephenie-lagrossa-s10","r":"same_person"},{"s":"person-stephenie-lagrossa","t":"contestant-stephenie-lagrossa-s11","r":"same_person"},{"s":"person-stephenie-lagrossa","t":"contestant-stephenie-lagrossa-s20","r":"same_person"},{"s":"person-tom-westman","t":"contestant-tom-westman-s10","r":"same_person"},{"s":"person-tom-westman","t":"contestant-tom-westman-s20","r":"same_person"},{"s":"person-danni-boatwright","t":"contestant-danni-boatwright-s11","r":"same_person"},{"s":"person-danni-boatwright","t":"contestant-danni-boatwright-s40","r":"same_person"},{"s":"person-cirie-fields","t":"contestant-cirie-fields-s12","r":"same_person"},{"s":"person-cirie-fields","t":"contestant-cirie-fields-s16","r":"same_person"},{"s":"person-cirie-fields","t":"contestant-cirie-fields-s20","r":"same_person"},{"s":"person-cirie-fields","t":"contestant-cirie-fields-s34","r":"same_person"},{"s":"person-terry-deitz","t":"contestant-terry-deitz-s12","r":"same_person"},{"s":"person-terry-deitz","t":"contestant-terry-deitz-s31","r":"same_person"},{"s":"person-danielle-dilorenzo","t":"contestant-danielle-dilorenzo-s12","r":"same_person"},{"s":"person-danielle-dilorenzo","t":"contestant-danielle-dilorenzo-s20","r":"same_person"},{"s":"person-aras-baskauskas","t":"contestant-aras-baskauskas-s12","r":"same_person"},{"s":"person-aras-baskauskas","t":"contestant-aras-baskauskas-s27","r":"same_person"},{"s":"person-candice-woodcock","t":"contestant-candice-woodcock-s13","r":"same_person"},{"s":"person-candice-woodcock","t":"contestant-candice-woodcock-s20","r":"same_person"},{"s":"person-jonathan-penner","t":"contestant-jonathan-penner-s13","r":"same_person"},{"s":"person-jonathan-penner","t":"contestant-jonathan-penner-s16","r":"same_person"},{"s":"person-jonathan-penner","t":"contestant-jonathan-penner-s25","r":"same_person"},{"s":"person-parvati-shallow","t":"contestant-parvati-shallow-s13","r":"same_person"},{"s":"person-parvati-shallow","t":"contestant-parvati-shallow-s16","r":"same_person"},{"s":"person-parvati-shallow","t":"contestant-parvati-shallow-s20","r":"same_person"},{"s":"person-parvati-shallow","t":"contestant-parvati-shallow-s40","r":"same_person"},{"s":"person-ozzy-lusth","t":"contestant-ozzy-lusth-s13","r":"same_person"},{"s":"person-ozzy-lusth","t":"contestant-ozzy-lusth-s16","r":"same_person"},{"s":"person-ozzy-lusth","t":"contestant-ozzy-lusth-s34","r":"same_person"},{"s":"person-yul-kwon","t":"contestant-yul-kwon-s13","r":"same_person"},{"s":"person-yul-kwon","t":"contestant-yul-kwon-s40","r":"same_person"},{"s":"person-yau-man-chan","t":"contestant-yau-man-chan-s14","r":"same_person"},{"s":"person-yau-man-chan","t":"contestant-yau-man-chan-s16","r":"same_person"},{"s":"person-james-clement","t":"contestant-james-clement-s15","r":"same_person"},{"s":"person-james-clement","t":"contestant-james-clement-s16","r":"same_person"},{"s":"person-james-clement","t":"contestant-james-clement-s20","r":"same_person"},{"s":"person-peih-gee-law","t":"contestant-peih-gee-law-s15","r":"same_person"},{"s":"person-peih-gee-law","t":"contestant-peih-gee-law-s31","r":"same_person"},{"s":"person-courtney-yates","t":"contestant-courtney-yates-s15","r":"same_person"},{"s":"person-courtney-yates","t":"contestant-courtney-yates-s20","r":"same_person"},{"s":"person-amanda-kimmel","t":"contestant-amanda-kimmel-s15","r":"same_person"},{"s":"person-amanda-kimmel","t":"contestant-amanda-kimmel-s16","r":"same_person"},{"s":"person-amanda-kimmel","t":"contestant-amanda-kimmel-s20","r":"same_person"},{"s":"person-erik-reichenbach","t":"contestant-erik-reichenbach-s16","r":"same_person"},{"s":"person-erik-reichenbach","t":"contestant-erik-reichenbach-s26","r":"same_person"},{"s":"person-randy-bailey","t":"contestant-randy-bailey-s17","r":"same_person"},{"s":"person-randy-bailey","t":"contestant-randy-bailey-s20","r":"same_person"},{"s":"person-corinne-kaplan","t":"contestant-corinne-kaplan-s17","r":"same_person"},{"s":"person-corinne-kaplan","t":"contestant-corinne-kaplan-s26","r":"same_person"},{"s":"person-sugar-kiper","t":"contestant-sugar-kiper-s17","r":"same_person"},{"s":"person-sugar-kiper","t":"contestant-sugar-kiper-s20","r":"same_person"},{"s":"person-tyson-apostol","t":"contestant-tyson-apostol-s18","r":"same_person"},{"s":"person-tyson-apostol","t":"contestant-tyson-apostol-s20","r":"same_person"},{"s":"person-tyson-apostol","t":"contestant-tyson-apostol-s27","r":"same_person"},{"s":"person-tyson-apostol","t":"contestant-tyson-apostol-s40","r":"same_person"},{"s":"person-coach-wade","t":"contestant-coach-wade-s18","r":"same_person"},{"s":"person-coach-wade","t":"contestant-coach-wade-s20","r":"same_person"},{"s":"person-coach-wade","t":"contestant-coach-wade-s23","r":"same_person"},{"s":"person-stephen-fishbach","t":"contestant-stephen-fishbach-s18","r":"same_person"},{"s":"person-stephen-fishbach","t":"contestant-stephen-fishbach-s31","r":"same_person"},{"s":"person-j-t-thomas","t":"contestant-j-t-thomas-s18","r":"same_person"},{"s":"person-j-t-thomas","t":"contestant-j-t-thomas-s20","r":"same_person"},{"s":"person-j-t-thomas","t":"contestant-j-t-thomas-s34","r":"same_person"},{"s":"person-russell-swan","t":"contestant-russell-swan-s19","r":"same_person"},{"s":"person-russell-swan","t":"contestant-russell-swan-s25","r":"same_person"},{"s":"person-laura-morett","t":"contestant-laura-morett-s19","r":"same_person"},{"s":"person-laura-morett","t":"contestant-laura-morett-s27","r":"same_person"},{"s":"person-monica-padilla","t":"contestant-monica-padilla-s19","r":"same_person"},{"s":"person-monica-padilla","t":"contestant-monica-padilla-s31","r":"same_person"},{"s":"person-russell-hantz","t":"contestant-russell-hantz-s19","r":"same_person"},{"s":"person-russell-hantz","t":"contestant-russell-hantz-s20","r":"same_person"},{"s":"person-russell-hantz","t":"contestant-russell-hantz-s22","r":"same_person"},{"s":"person-brenda-lowe","t":"contestant-brenda-lowe-s21","r":"same_person"},{"s":"person-brenda-lowe","t":"contestant-brenda-lowe-s26","r":"same_person"},{"s":"person-francesca-hogi","t":"contestant-francesca-hogi-s22","r":"same_person"},{"s":"person-francesca-hogi","t":"contestant-francesca-hogi-s26","r":"same_person"},{"s":"person-matt-elrod","t":"contestant-matt-elrod-s22","r":"same_person"},{"s":"person-matt-elrod","t":"contestant-matt-elrod-s22","r":"same_person"},{"s":"person-andrea-boehlke","t":"contestant-andrea-boehlke-s22","r":"same_person"},{"s":"person-andrea-boehlke","t":"contestant-andrea-boehlke-s26","r":"same_person"},{"s":"person-andrea-boehlke","t":"contestant-andrea-boehlke-s34","r":"same_person"},{"s":"person-phillip-sheppard","t":"contestant-phillip-sheppard-s22","r":"same_person"},{"s":"person-phillip-sheppard","t":"contestant-phillip-sheppard-s26","r":"same_person"},{"s":"person-christine-shields-markoski","t":"contestant-christine-shields-markoski-s23","r":"same_person"},{"s":"person-christine-shields-markoski","t":"contestant-christine-shields-markoski-s23","r":"same_person"},{"s":"person-rick-nelson","t":"contestant-rick-nelson-s23","r":"same_person"},{"s":"person-rick-nelson","t":"contestant-rick-nelson-s23","r":"same_person"},{"s":"person-dawn-meehan","t":"contestant-dawn-meehan-s23","r":"same_person"},{"s":"person-dawn-meehan","t":"contestant-dawn-meehan-s26","r":"same_person"},{"s":"person-brandon-hantz","t":"contestant-brandon-hantz-s23","r":"same_person"},{"s":"person-brandon-hantz","t":"contestant-brandon-hantz-s26","r":"same_person"},{"s":"person-sophie-clarke","t":"contestant-sophie-clarke-s23","r":"same_person"},{"s":"person-sophie-clarke","t":"contestant-sophie-clarke-s40","r":"same_person"},{"s":"person-monica-culpepper","t":"contestant-monica-culpepper-s24","r":"same_person"},{"s":"person-monica-culpepper","t":"contestant-monica-culpepper-s27","r":"same_person"},{"s":"person-troyzan-robertson","t":"contestant-troyzan-robertson-s24","r":"same_person"},{"s":"person-troyzan-robertson","t":"contestant-troyzan-robertson-s34","r":"same_person"},{"s":"person-kat-edorsson","t":"contestant-kat-edorsson-s24","r":"same_person"},{"s":"person-kat-edorsson","t":"contestant-kat-edorsson-s27","r":"same_person"},{"s":"person-abi-maria-gomes","t":"contestant-abi-maria-gomes-s25","r":"same_person"},{"s":"person-abi-maria-gomes","t":"contestant-abi-maria-gomes-s31","r":"same_person"},{"s":"person-malcolm-freberg","t":"contestant-malcolm-freberg-s25","r":"same_person"},{"s":"person-malcolm-freberg","t":"contestant-malcolm-freberg-s26","r":"same_person"},{"s":"person-malcolm-freberg","t":"contestant-malcolm-freberg-s34","r":"same_person"},{"s":"person-denise-stapley","t":"contestant-denise-stapley-s25","r":"same_person"},{"s":"person-denise-stapley","t":"contestant-denise-stapley-s40","r":"same_person"},{"s":"person-john-cody","t":"contestant-john-cody-s27","r":"same_person"},{"s":"person-john-cody","t":"contestant-john-cody-s27","r":"same_person"},{"s":"person-brad-culpepper","t":"contestant-brad-culpepper-s27","r":"same_person"},{"s":"person-brad-culpepper","t":"contestant-brad-culpepper-s34","r":"same_person"},{"s":"person-vytas-baskauskas","t":"contestant-vytas-baskauskas-s27","r":"same_person"},{"s":"person-vytas-baskauskas","t":"contestant-vytas-baskauskas-s31","r":"same_person"},{"s":"person-ciera-eastin","t":"contestant-ciera-eastin-s27","r":"same_person"},{"s":"person-ciera-eastin","t":"contestant-ciera-eastin-s31","r":"same_person"},{"s":"person-ciera-eastin","t":"contestant-ciera-eastin-s34","r":"same_person"},{"s":"person-sarah-lacina","t":"contestant-sarah-lacina-s28","r":"same_person"},{"s":"person-sarah-lacina","t":"contestant-sarah-lacina-s34","r":"same_person"},{"s":"person-sarah-lacina","t":"contestant-sarah-lacina-s40","r":"same_person"},{"s":"person-tasha-fox","t":"contestant-tasha-fox-s28","r":"same_person"},{"s":"person-tasha-fox","t":"contestant-tasha-fox-s31","r":"same_person"},{"s":"person-spencer-bledsoe","t":"contestant-spencer-bledsoe-s28","r":"same_person"},{"s":"person-spencer-bledsoe","t":"contestant-spencer-bledsoe-s31","r":"same_person"},{"s":"person-kass-mcquillen","t":"contestant-kass-mcquillen-s28","r":"same_person"},{"s":"person-kass-mcquillen","t":"contestant-kass-mcquillen-s31","r":"same_person"},{"s":"person-tony-vlachos","t":"contestant-tony-vlachos-s28","r":"same_person"},{"s":"person-tony-vlachos","t":"contestant-tony-vlachos-s34","r":"same_person"},{"s":"person-tony-vlachos","t":"contestant-tony-vlachos-s40","r":"same_person"},{"s":"person-kelley-wentworth","t":"contestant-kelley-wentworth-s29","r":"same_person"},{"s":"person-kelley-wentworth","t":"contestant-kelley-wentworth-s31","r":"same_person"},{"s":"person-kelley-wentworth","t":"contestant-kelley-wentworth-s38","r":"same_person"},{"s":"person-jeremy-collins","t":"contestant-jeremy-collins-s29","r":"same_person"},{"s":"person-jeremy-collins","t":"contestant-jeremy-collins-s31","r":"same_person"},{"s":"person-jeremy-collins","t":"contestant-jeremy-collins-s40","r":"same_person"},{"s":"person-keith-nale","t":"contestant-keith-nale-s29","r":"same_person"},{"s":"person-keith-nale","t":"contestant-keith-nale-s31","r":"same_person"},{"s":"person-natalie-anderson","t":"contestant-natalie-anderson-s29","r":"same_person"},{"s":"person-natalie-anderson","t":"contestant-natalie-anderson-s40","r":"same_person"},{"s":"person-hali-ford","t":"contestant-hali-ford-s30","r":"same_person"},{"s":"person-hali-ford","t":"contestant-hali-ford-s34","r":"same_person"},{"s":"person-joe-anglim","t":"contestant-joe-anglim-s30","r":"same_person"},{"s":"person-joe-anglim","t":"contestant-joe-anglim-s31","r":"same_person"},{"s":"person-joe-anglim","t":"contestant-joe-anglim-s38","r":"same_person"},{"s":"person-shirin-oskooi","t":"contestant-shirin-oskooi-s30","r":"same_person"},{"s":"person-shirin-oskooi","t":"contestant-shirin-oskooi-s31","r":"same_person"},{"s":"person-sierra-dawn-thomas","t":"contestant-sierra-dawn-thomas-s30","r":"same_person"},{"s":"person-sierra-dawn-thomas","t":"contestant-sierra-dawn-thomas-s34","r":"same_person"},{"s":"person-caleb-reynolds","t":"contestant-caleb-reynolds-s32","r":"same_person"},{"s":"person-caleb-reynolds","t":"contestant-caleb-reynolds-s34","r":"same_person"},{"s":"person-debbie-wanner","t":"contestant-debbie-wanner-s32","r":"same_person"},{"s":"person-debbie-wanner","t":"contestant-debbie-wanner-s34","r":"same_person"},{"s":"person-tai-trang","t":"contestant-tai-trang-s32","r":"same_person"},{"s":"person-tai-trang","t":"contestant-tai-trang-s34","r":"same_person"},{"s":"person-aubry-bracco","t":"contestant-aubry-bracco-s32","r":"same_person"},{"s":"person-aubry-bracco","t":"contestant-aubry-bracco-s34","r":"same_person"},{"s":"person-aubry-bracco","t":"contestant-aubry-bracco-s38","r":"same_person"},{"s":"person-michele-fitzgerald","t":"contestant-michele-fitzgerald-s32","r":"same_person"},{"s":"person-michele-fitzgerald","t":"contestant-michele-fitzgerald-s40","r":"same_person"},{"s":"person-michaela-bradshaw","t":"contestant-michaela-bradshaw-s33","r":"same_person"},{"s":"person-michaela-bradshaw","t":"contestant-michaela-bradshaw-s34","r":"same_person"},{"s":"person-zeke-smith","t":"contestant-zeke-smith-s33","r":"same_person"},{"s":"person-zeke-smith","t":"contestant-zeke-smith-s34","r":"same_person"},{"s":"person-david-wright","t":"contestant-david-wright-s33","r":"same_person"},{"s":"person-david-wright","t":"contestant-david-wright-s38","r":"same_person"},{"s":"person-adam-klein","t":"contestant-adam-klein-s33","r":"same_person"},{"s":"person-adam-klein","t":"contestant-adam-klein-s40","r":"same_person"},{"s":"person-ben-driebergen","t":"contestant-ben-driebergen-s35","r":"same_person"},{"s":"person-ben-driebergen","t":"contestant-ben-driebergen-s40","r":"same_person"},{"s":"person-wendell-holland","t":"contestant-wendell-holland-s36","r":"same_person"},{"s":"person-wendell-holland","t":"contestant-wendell-holland-s40","r":"same_person"},{"s":"person-nick-wilson","t":"contestant-nick-wilson-s37","r":"same_person"},{"s":"person-nick-wilson","t":"contestant-nick-wilson-s40","r":"same_person"},{"s":"person-chris-underwood","t":"contestant-chris-underwood-s38","r":"same_person"},{"s":"person-chris-underwood","t":"contestant-chris-underwood-s38","r":"same_person"},{"s":"person-rick-devens","t":"contestant-rick-devens-s38","r":"same_person"},{"s":"person-rick-devens","t":"contestant-rick-devens-s38","r":"same_person"},{"s":"person-owen-knight","t":"contestant-owen-knight-s43","r":"same_person"},{"s":"person-owen-knight","t":"contestant-owen-knight-s43","r":"same_person"},{"s":"person-bruce-perreault","t":"contestant-bruce-perreault-s44","r":"same_person"},{"s":"person-bruce-perreault","t":"contestant-bruce-perreault-s45","r":"same_person"},{"s":"person-brandon-cottom","t":"contestant-brandon-cottom-s44","r":"same_person"},{"s":"person-brandon-cottom","t":"contestant-brandon-cottom-s44","r":"same_person"},{"s":"person-teeny-chirichillo","t":"contestant-teeny-chirichillo-s47","r":"same_person"},{"s":"person-teeny-chirichillo","t":"contestant-teeny-chirichillo-s49","r":"same_person"},{"s":"person-rachel-lamont","t":"contestant-rachel-lamont-s47","r":"same_person"},{"s":"person-rachel-lamont","t":"contestant-rachel-lamont-s47","r":"same_person"}]}};

const ERA_C = {classic:"#E5A100",modern:"#8B5CF6",new_era:"#00C896"};
const ERA_L = {classic:"Classic (1-20)",modern:"Modern (21-40)",new_era:"New Era (41-50)"};
const NODE_C = {S:"#E5A100",P:"#00B4D8"};
const TABS = ["Overview","Seasons","Players","Graph Explorer","Data Quality"];

const QUERIES = [
  {label:"All seasons + returning player connections",filter:()=>true},
  {label:"Classic era only (S1-S20)",filter:n=>n.t==="S"?n.era==="classic":n.ss?.some(s=>s<=20)},
  {label:"Modern era only (S21-S40)",filter:n=>n.t==="S"?n.era==="modern":n.ss?.some(s=>s>20&&s<=40)},
  {label:"New Era only (S41-S50)",filter:n=>n.t==="S"?n.era==="new_era":n.ss?.some(s=>s>40)},
  {label:"Players with 4+ appearances",filter:n=>n.t==="P"?n.tp>=4:true},
  {label:"Players with 3+ appearances",filter:n=>n.t==="P"?n.tp>=3:true},
  {label:"Seasons with unanimous winners",filter:n=>{if(n.t!=="S")return false;return n.v&&n.v.includes("-0")}},
];

function Tip({active,payload:pl}){
  if(!active||!pl?.length)return null;
  const d=pl[0]?.payload;
  return <div style={{background:"#14151f",border:"1px solid #2a2b3a",borderRadius:6,padding:"8px 12px",fontSize:11,color:"#999",maxWidth:240,boxShadow:"0 8px 32px #00000080"}}>
    <div style={{fontWeight:700,color:"#e0e0f0",marginBottom:3}}>{d?.label||d?.name||`S${d?.n}`}</div>
    {pl.map((p,i)=><div key={i} style={{color:p.color||"#888"}}>{p.name}: {typeof p.value==="number"?p.value.toFixed?.(1)??p.value:p.value}</div>)}
  </div>;
}

function KPI({label,value,sub,color="#E5A100"}){
  return <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:"10px 14px",flex:"1 1 120px",position:"relative",overflow:"hidden"}}>
    <div style={{position:"absolute",top:0,left:0,width:3,height:"100%",background:color,borderRadius:"8px 0 0 8px"}}/>
    <div style={{fontSize:9,color:"#555",textTransform:"uppercase",letterSpacing:"0.08em",marginBottom:2}}>{label}</div>
    <div style={{fontSize:22,fontWeight:800,color:"#e0e0f0",lineHeight:1.1}}>{value}</div>
    {sub&&<div style={{fontSize:9,color:"#444",marginTop:2}}>{sub}</div>}
  </div>;
}

function GraphCanvas({query,onSelect}){
  const svgRef=useRef(null);
  const simRef=useRef(null);
  const [nodes,setNodes]=useState([]);
  const [edges,setEdges]=useState([]);
  const [sel,setSel]=useState(null);

  useEffect(()=>{
    const raw=D.graph;
    const filter=QUERIES[query]?.filter||(()=>true);
    const ns=raw.n.filter(filter).map(n=>({...n,x:Math.random()*600-300,y:Math.random()*400-200,
      radius:n.t==="S"?10:5+(n.tp||1)*1.2,color:n.t==="S"?(ERA_C[n.era]||"#666"):NODE_C.P}));
    const nids=new Set(ns.map(n=>n.id));
    const es=raw.e.filter(e=>nids.has(e.s)&&nids.has(e.t)).map(e=>({source:e.s,target:e.t,type:e.r}));
    setNodes(ns);setEdges(es);

    if(simRef.current)simRef.current.stop();
    const sim=d3.forceSimulation(ns)
      .force("link",d3.forceLink(es).id(d=>d.id).distance(d=>d.type==="same_person"?25:70).strength(d=>d.type==="same_person"?0.9:0.12))
      .force("charge",d3.forceManyBody().strength(d=>d.t==="S"?-180:-40))
      .force("center",d3.forceCenter(0,0))
      .force("collision",d3.forceCollide().radius(d=>d.radius+2))
      .alphaDecay(0.025)
      .on("tick",()=>setNodes(p=>[...p]));
    simRef.current=sim;
    return()=>sim.stop();
  },[query]);

  const handleClick=(n)=>{setSel(n.id===sel?null:n.id);onSelect?.(n);};
  const nodeMap=useMemo(()=>new Map(nodes.map(n=>[n.id,n])),[nodes]);

  return <div style={{position:"relative",width:"100%",height:"100%"}}>
    <svg ref={svgRef} style={{width:"100%",height:"100%",background:"#0c0d14"}}
      viewBox="-350 -250 700 500" preserveAspectRatio="xMidYMid meet">
      <defs><filter id="glow2"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
      {edges.map((e,i)=>{
        const s=typeof e.source==="object"?e.source:nodeMap.get(e.source);
        const t=typeof e.target==="object"?e.target:nodeMap.get(e.target);
        if(!s||!t)return null;
        const hi=sel&&(s.id===sel||t.id===sel);
        return <line key={i} x1={s.x||0} y1={s.y||0} x2={t.x||0} y2={t.y||0}
          stroke={hi?"#E5A100":e.type==="returning_player"?"#E5A10044":"#ffffff06"}
          strokeWidth={hi?1.5:e.type==="returning_player"?0.6:0.2}/>;
      })}
      {nodes.map(n=><g key={n.id} transform={`translate(${n.x||0},${n.y||0})`} onClick={()=>handleClick(n)} style={{cursor:"pointer"}}>
        {sel===n.id&&<circle r={n.radius+5} fill="none" stroke="#E5A100" strokeWidth={1.5} opacity={0.5}/>}
        <circle r={n.radius} fill={n.color} opacity={sel&&sel!==n.id?0.25:0.85}/>
        {n.t==="S"&&<text y={n.radius+9} textAnchor="middle" fill={sel===n.id?"#E5A100":"#444"} fontSize={5.5} fontFamily="inherit">{n.l.split(":")[0]}</text>}
        {n.t==="P"&&n.tp>=4&&<text y={n.radius+8} textAnchor="middle" fill="#00B4D888" fontSize={4.5} fontFamily="inherit">{n.l.split(" ").pop()}</text>}
      </g>)}
    </svg>
    {sel&&nodeMap.get(sel)&&<div style={{position:"absolute",top:8,right:8,width:180,background:"#14151fEE",border:"1px solid #2a2b3a",borderRadius:8,padding:10,fontSize:10,color:"#999",backdropFilter:"blur(8px)"}}>
      <div style={{fontSize:8,color:"#555",textTransform:"uppercase",letterSpacing:"0.1em"}}>{nodeMap.get(sel).t==="S"?"Season":"Player"}</div>
      <div style={{fontSize:13,fontWeight:700,color:nodeMap.get(sel).color,margin:"4px 0"}}>{nodeMap.get(sel).l}</div>
      {nodeMap.get(sel).t==="S"&&<><div>Winner: {nodeMap.get(sel).w}</div><div>FTC: {nodeMap.get(sel).v}</div><div>Era: {nodeMap.get(sel).era}</div></>}
      {nodeMap.get(sel).t==="P"&&<><div>Times played: {nodeMap.get(sel).tp}</div><div>Seasons: {nodeMap.get(sel).ss?.join(", ")}</div></>}
      <button onClick={()=>setSel(null)} style={{marginTop:6,padding:"3px 6px",fontSize:8,background:"#1e1f2e",border:"1px solid #2a2b3a",borderRadius:3,color:"#666",cursor:"pointer",fontFamily:"inherit",width:"100%"}}>Clear</button>
    </div>}
  </div>;
}

export default function Dashboard(){
  const [tab,setTab]=useState(0);
  const [gQuery,setGQuery]=useState(0);
  const [gNode,setGNode]=useState(null);

  const viewData=useMemo(()=>D.seasons.filter(s=>s.avgV>0).map(s=>({...s,label:`S${s.n}`})),[]);
  const eraData=useMemo(()=>Object.entries(D.eras).map(([k,v])=>({name:ERA_L[k]||k,value:v,color:ERA_C[k]})),[]);
  const elimData=useMemo(()=>Object.entries(D.elimMethods).sort((a,b)=>b[1]-a[1]).map(([k,v])=>({name:k,value:v})),[]);
  const chalData=useMemo(()=>Object.entries(D.challengeTypes).map(([k,v])=>({name:k,value:v})),[]);
  const marginData=useMemo(()=>{
    const byEra={classic:[],modern:[],new_era:[]};
    D.seasons.forEach(s=>{if(s.vote){const parts=s.vote.split("-").map(Number);const margin=parts[0]-(parts[1]||0);if(!isNaN(margin))byEra[s.era]?.push(margin);}});
    return Object.entries(byEra).map(([k,v])=>({era:ERA_L[k],avg:v.length?+(v.reduce((a,b)=>a+b,0)/v.length).toFixed(1):0,color:ERA_C[k]}));
  },[]);
  const mechData=useMemo(()=>D.seasons.map(s=>({label:`S${s.n}`,mechs:s.mechs,era:s.era})),[]);
  const radarData=useMemo(()=>{
    const q=D.quality;const t=q.total;
    return [{field:"Titles",v:Math.round(q.title/t*100)},{field:"Dates",v:Math.round(q.date/t*100)},{field:"Tribal",v:Math.round(q.tc/t*100)},{field:"Challenges",v:Math.round(q.chal/t*100)},{field:"Viewership",v:Math.round(q.view/t*100)},{field:"Notable",v:Math.round(q.notable/t*100)},{field:"Detailed",v:Math.round(q.detailed/t*100)}];
  },[]);

  const ELIM_COLORS=["#E5A100","#00B4D8","#E54040","#00C896","#8B5CF6","#FF6B6B","#4ECDC4"];

  return <div style={{background:"#0a0b10",color:"#c0c0d0",fontFamily:"'DM Mono','Fira Code',monospace",height:"100vh",display:"flex",overflow:"hidden"}}>
    {/* Sidebar */}
    <div style={{width:52,background:"#0e0f18",borderRight:"1px solid #1a1b28",display:"flex",flexDirection:"column",alignItems:"center",paddingTop:12,gap:2,flexShrink:0}}>
      <div style={{width:28,height:28,borderRadius:6,background:"linear-gradient(135deg,#E5A100,#E54040)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:12,fontWeight:900,color:"#0a0b10",marginBottom:12}}>S</div>
      {TABS.map((t,i)=><button key={i} onClick={()=>setTab(i)} title={t}
        style={{width:36,height:36,borderRadius:6,border:"none",background:tab===i?"#1e1f2e":"transparent",color:tab===i?"#E5A100":"#444",cursor:"pointer",fontSize:14,display:"flex",alignItems:"center",justifyContent:"center",fontFamily:"inherit",transition:"all 0.15s"}}>
        {["◉","▥","◎","◈","◇"][i]}
      </button>)}
      <div style={{flex:1}}/>
      <div style={{fontSize:7,color:"#2a2b3a",writingMode:"vertical-rl",transform:"rotate(180deg)",paddingBottom:12,letterSpacing:"0.1em"}}>v0.5.0</div>
    </div>

    {/* Main */}
    <div style={{flex:1,display:"flex",flexDirection:"column",overflow:"hidden"}}>
      {/* Top bar */}
      <div style={{padding:"8px 16px",borderBottom:"1px solid #1a1b28",display:"flex",alignItems:"center",gap:12,flexShrink:0,background:"#0e0f18"}}>
        <div style={{fontSize:12,fontWeight:800,letterSpacing:"0.05em"}}>
          <span style={{color:"#E5A100"}}>SURVIVOR</span>
          <span style={{color:"#555",marginLeft:6}}>KNOWLEDGE GRAPH</span>
        </div>
        <div style={{flex:1}}/>
        <div style={{fontSize:8,color:"#333"}}>18,868 TRIPLES</div>
        <div style={{width:1,height:12,background:"#222"}}/>
        <div style={{fontSize:8,color:"#333"}}>749 GRAPHS</div>
        <div style={{width:1,height:12,background:"#222"}}/>
        <div style={{fontSize:8,color:"#333"}}>44 TESTS</div>
      </div>

      {/* Tab title */}
      <div style={{padding:"10px 16px 6px",fontSize:11,fontWeight:700,color:"#888",letterSpacing:"0.08em",textTransform:"uppercase",flexShrink:0}}>{TABS[tab]}</div>

      {/* Content */}
      <div style={{flex:1,overflow:"auto",padding:"0 16px 16px"}}>

        {tab===0&&<div>
          {/* KPI ribbon */}
          <div style={{display:"flex",gap:8,marginBottom:12,flexWrap:"wrap"}}>
            <KPI label="Seasons" value="50" sub="2000-2026" color="#E5A100"/>
            <KPI label="Contestants" value="728" sub="98 returning" color="#00B4D8"/>
            <KPI label="Episodes" value="699" sub="642 detailed" color="#00C896"/>
            <KPI label="RDF Triples" value="18.9K" sub="749 named graphs" color="#8B5CF6"/>
            <KPI label="Coverage" value="92%" sub="tribal councils" color="#E54040"/>
            <KPI label="Sources" value="12" sub="tracked with PROV-O" color="#555"/>
          </div>

          {/* Charts row 1 */}
          <div style={{display:"grid",gridTemplateColumns:"2fr 1fr",gap:12,marginBottom:12}}>
            <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
              <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>VIEWERSHIP DECLINE (millions)</div>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={viewData} margin={{left:-15}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1a1b2a" vertical={false}/>
                  <XAxis dataKey="label" tick={{fontSize:7,fill:"#333"}} interval={4}/>
                  <YAxis tick={{fontSize:8,fill:"#444"}}/>
                  <Tooltip content={<Tip/>}/>
                  <Bar dataKey="avgV" name="Avg Viewers (M)" radius={[2,2,0,0]}>
                    {viewData.map((s,i)=><Cell key={i} fill={ERA_C[s.era]} opacity={0.8}/>)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
              <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>ERA DISTRIBUTION</div>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={eraData} cx="50%" cy="50%" innerRadius={45} outerRadius={75} dataKey="value" label={({name,value})=>`${value}`} labelLine={false}>
                    {eraData.map((e,i)=><Cell key={i} fill={e.color} stroke="#0a0b10" strokeWidth={2}/>)}
                  </Pie>
                  <Tooltip/>
                  <Legend wrapperStyle={{fontSize:9}}/>
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Charts row 2 */}
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
            <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
              <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>ELIMINATION METHODS</div>
              <ResponsiveContainer width="100%" height={180}>
                <PieChart>
                  <Pie data={elimData} cx="50%" cy="50%" outerRadius={65} dataKey="value" label={({name,percent})=>`${name} ${(percent*100).toFixed(0)}%`} labelLine={false}>
                    {elimData.map((e,i)=><Cell key={i} fill={ELIM_COLORS[i%ELIM_COLORS.length]} opacity={0.8}/>)}
                  </Pie>
                  <Tooltip/>
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
              <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>FTC VOTE MARGIN BY ERA</div>
              <ResponsiveContainer width="100%" height={180}>
                <BarChart data={marginData} layout="vertical" margin={{left:10}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1a1b2a" horizontal={false}/>
                  <XAxis type="number" tick={{fontSize:9,fill:"#444"}}/>
                  <YAxis type="category" dataKey="era" tick={{fontSize:8,fill:"#555"}} width={100}/>
                  <Tooltip content={<Tip/>}/>
                  <Bar dataKey="avg" name="Avg Margin" radius={[0,4,4,0]}>
                    {marginData.map((m,i)=><Cell key={i} fill={m.color}/>)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>}

        {tab===1&&<div>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12,marginBottom:12}}>
            <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
              <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>CAST SIZE BY SEASON</div>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={D.seasons.map(s=>({...s,label:`S${s.n}`}))}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1a1b2a" vertical={false}/>
                  <XAxis dataKey="label" tick={{fontSize:6,fill:"#333"}} interval={4}/>
                  <YAxis tick={{fontSize:8,fill:"#444"}} domain={[12,26]}/>
                  <Tooltip content={<Tip/>}/>
                  <Bar dataKey="cast" name="Cast Size" radius={[2,2,0,0]}>
                    {D.seasons.map((s,i)=><Cell key={i} fill={ERA_C[s.era]} opacity={0.7}/>)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
              <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>GAME DAYS BY SEASON</div>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={D.seasons.map(s=>({...s,label:`S${s.n}`}))}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1a1b2a" vertical={false}/>
                  <XAxis dataKey="label" tick={{fontSize:6,fill:"#333"}} interval={4}/>
                  <YAxis tick={{fontSize:8,fill:"#444"}} domain={[24,44]}/>
                  <Tooltip content={<Tip/>}/>
                  <Line type="stepAfter" dataKey="days" stroke="#E5A100" strokeWidth={2} dot={{r:2,fill:"#E5A100"}}/>
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
            <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>MECHANICS DENSITY BY SEASON</div>
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={mechData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1a1b2a" vertical={false}/>
                <XAxis dataKey="label" tick={{fontSize:6,fill:"#333"}} interval={4}/>
                <YAxis tick={{fontSize:8,fill:"#444"}}/>
                <Tooltip content={<Tip/>}/>
                <Bar dataKey="mechs" name="Mechanics" radius={[2,2,0,0]}>
                  {mechData.map((m,i)=><Cell key={i} fill={ERA_C[m.era]} opacity={0.7}/>)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          {/* Season table */}
          <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14,marginTop:12,maxHeight:250,overflow:"auto"}}>
            <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>ALL SEASONS</div>
            <table style={{width:"100%",borderCollapse:"collapse",fontSize:9}}>
              <thead><tr style={{color:"#555",borderBottom:"1px solid #1e1f2e"}}>
                <th style={{textAlign:"left",padding:"4px 6px"}}>#</th><th style={{textAlign:"left",padding:"4px 6px"}}>Name</th><th>Winner</th><th>Vote</th><th>Cast</th><th>Days</th><th>Avg M</th>
              </tr></thead>
              <tbody>{D.seasons.map(s=><tr key={s.n} style={{borderBottom:"1px solid #14151f",color:"#888"}}>
                <td style={{padding:"3px 6px",color:ERA_C[s.era],fontWeight:700}}>S{s.n}</td>
                <td style={{padding:"3px 6px",maxWidth:140,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{s.name}</td>
                <td style={{padding:"3px 6px",textAlign:"center"}}>{s.winner.split(" ").pop()}</td>
                <td style={{padding:"3px 6px",textAlign:"center",color:"#555"}}>{s.vote}</td>
                <td style={{padding:"3px 6px",textAlign:"center"}}>{s.cast}</td>
                <td style={{padding:"3px 6px",textAlign:"center"}}>{s.days}</td>
                <td style={{padding:"3px 6px",textAlign:"center"}}>{s.avgV||""}</td>
              </tr>)}</tbody>
            </table>
          </div>
        </div>}

        {tab===2&&<div>
          <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14,marginBottom:12}}>
            <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>TOP RETURNING PLAYERS (by appearances)</div>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={D.returners.slice(0,15)} layout="vertical" margin={{left:10}}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1a1b2a" horizontal={false}/>
                <XAxis type="number" tick={{fontSize:9,fill:"#444"}} domain={[0,6]}/>
                <YAxis type="category" dataKey="name" tick={{fontSize:8,fill:"#888"}} width={130}/>
                <Tooltip content={<Tip/>}/>
                <Bar dataKey="tp" name="Times Played" radius={[0,4,4,0]} fill="#00B4D8" opacity={0.8}/>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
            <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>RETURNING PLAYER SEASONS</div>
            <div style={{maxHeight:200,overflow:"auto"}}>
              {D.returners.map(p=><div key={p.name} style={{display:"flex",alignItems:"center",gap:8,padding:"4px 0",borderBottom:"1px solid #14151f"}}>
                <div style={{width:120,fontSize:9,color:"#888",flexShrink:0}}>{p.name}</div>
                <div style={{display:"flex",gap:3,flexWrap:"wrap"}}>
                  {p.ss.map(sn=><div key={sn} style={{padding:"1px 5px",fontSize:8,background:ERA_C[sn<=20?"classic":sn<=40?"modern":"new_era"]+"22",border:`1px solid ${ERA_C[sn<=20?"classic":sn<=40?"modern":"new_era"]}44`,borderRadius:3,color:ERA_C[sn<=20?"classic":sn<=40?"modern":"new_era"]}}>S{sn}</div>)}
                </div>
              </div>)}
            </div>
          </div>
        </div>}

        {tab===3&&<div>
          <div style={{display:"flex",gap:8,marginBottom:8,alignItems:"center"}}>
            <div style={{fontSize:9,color:"#555"}}>Query:</div>
            <select value={gQuery} onChange={e=>setGQuery(Number(e.target.value))}
              style={{background:"#12131d",border:"1px solid #2a2b3a",borderRadius:4,padding:"4px 8px",color:"#aaa",fontSize:10,fontFamily:"inherit",flex:1,maxWidth:400,outline:"none"}}>
              {QUERIES.map((q,i)=><option key={i} value={i}>{q.label}</option>)}
            </select>
            <div style={{fontSize:8,color:"#333"}}>{D.graph.n.filter(QUERIES[gQuery].filter).length} nodes</div>
          </div>
          <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,overflow:"hidden",height:"calc(100vh - 180px)"}}>
            <GraphCanvas query={gQuery} onSelect={setGNode}/>
          </div>
        </div>}

        {tab===4&&<div>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12,marginBottom:12}}>
            <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
              <div style={{fontSize:10,color:"#555",marginBottom:10,fontWeight:600}}>FIELD COVERAGE (699 episodes)</div>
              {[{l:"Titles",v:D.quality.title,c:"#00C896"},{l:"Air dates",v:D.quality.date,c:"#00C896"},
                {l:"Tribal councils",v:D.quality.tc,c:"#00C896"},{l:"Viewership",v:D.quality.view,c:"#E5A100"},
                {l:"Challenges",v:D.quality.chal,c:"#E54040"},{l:"Notable events",v:D.quality.notable,c:"#E54040"},
                {l:"Detailed",v:D.quality.detailed,c:"#00B4D8"}
              ].map((x,i)=><div key={i} style={{display:"flex",alignItems:"center",gap:8,marginBottom:6}}>
                <span style={{width:90,fontSize:9,color:"#666"}}>{x.l}</span>
                <div style={{flex:1,height:8,background:"#1a1b2a",borderRadius:4,overflow:"hidden"}}>
                  <div style={{width:`${x.v/D.quality.total*100}%`,height:"100%",background:x.c,borderRadius:4,transition:"width 0.5s"}}/>
                </div>
                <span style={{width:60,fontSize:9,color:"#555",textAlign:"right"}}>{x.v}/{D.quality.total}</span>
              </div>)}
            </div>
            <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
              <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>DATA QUALITY RADAR</div>
              <ResponsiveContainer width="100%" height={220}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#1e1f2e"/>
                  <PolarAngleAxis dataKey="field" tick={{fontSize:8,fill:"#555"}}/>
                  <PolarRadiusAxis tick={{fontSize:7,fill:"#333"}} domain={[0,100]}/>
                  <Radar name="Coverage %" dataKey="v" stroke="#E5A100" fill="#E5A100" fillOpacity={0.15} strokeWidth={2}/>
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
            <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
              <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>COMPLETENESS TIERS</div>
              <ResponsiveContainer width="100%" height={160}>
                <PieChart>
                  <Pie data={[{name:"Detailed",value:D.quality.detailed},{name:"Season-level",value:D.quality["season-level"]||0},{name:"Stub",value:D.quality.stub||0}]}
                    cx="50%" cy="50%" innerRadius={35} outerRadius={60} dataKey="value" label={({name,value})=>`${name}: ${value}`} labelLine={false}>
                    <Cell fill="#00C896"/><Cell fill="#E5A100"/><Cell fill="#E54040"/>
                  </Pie>
                  <Tooltip/>
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div style={{background:"#12131d",border:"1px solid #1e1f2e",borderRadius:8,padding:14}}>
              <div style={{fontSize:10,color:"#555",marginBottom:8,fontWeight:600}}>PROVENANCE</div>
              <div style={{fontSize:10,color:"#888",lineHeight:1.8}}>
                <div>Sources tracked: <span style={{color:"#E5A100",fontWeight:700}}>12</span></div>
                <div>Per-season records: <span style={{color:"#00C896"}}>50/50</span></div>
                <div>Per-episode records: <span style={{color:"#00C896"}}>699/699</span></div>
                <div>Enrichment phases: <span style={{color:"#00B4D8"}}>8</span></div>
                <div>Avg confidence: <span style={{color:"#E5A100"}}>0.899</span></div>
                <div>Highest: epguides.com (<span style={{color:"#00C896"}}>0.98</span>)</div>
                <div>Lowest: algorithmic (<span style={{color:"#E54040"}}>0.80</span>)</div>
              </div>
            </div>
          </div>
        </div>}
      </div>
    </div>
  </div>;
}