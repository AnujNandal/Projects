function search()
{
	var srch = document.getElementById("srchbox").value;
	if (srch == "" || srch == null)
	{
		alert("Please enter the name of a state,\ncity, airport, neighborhood,\nlandmark, or property to proceed.");
		return false;
	}		
}

const locations = [
	{name: 'Rajasthan'},
	{name: 'Agra'},
	{name: 'Kerala'},
	{name: 'Varanasi'},
	{name: 'Delhi'},
	{name: 'Goa'}
];	
	
const sboxtext = document.querySelector('.sboxtext');
const suggestionsPanel = document.querySelector('.suggestions');

sboxtext.addEventListener('keyup', function() {
	const input = sboxtext.value;
	suggestionsPanel.innerHTML = '';
	const suggestions = locations.filter(function(location) {
		return location.name.toLowerCase().startsWith(input);
	});
	suggestions.forEach(function(suggested) {
		const div = document.createElement('div');
		div.innerHTML = suggested.name;
		suggestionsPanel.appendChild(div);
	});
	if (input === '') {
		suggestionsPanel.innerHTML = '';
	}		
})

function initMap() {
  const uluru = { lat: -25.344, lng: 131.036 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: uluru,
  });
  const marker = new google.maps.Marker({
    position: uluru,
    map: map,
  });
}

function fhsearch()
{
	var srch = document.getElementById("srchbox").value;
	if (srch == "" || srch == null)
	{
		alert("Please enter the name of a destination,\nplace, airport, area,\nlandmark, or monument to proceed.");
		return false;
	}		
}

function hhsearch()
{
	var srch = document.getElementById("srchbox").value;
	if (srch == "" || srch == null)
	{
		alert("Please enter the name of a property,\nplace, area, district,\nlandmark, or monument to proceed.");
		return false;
	}		
}

function fsearch()
{
	var srch = document.getElementById("srchbox").value;
	if (srch == "" || srch == null)
	{
		alert("Please enter the name of a destination,\nstate, airport, area,\nlandmark, or property to proceed.");
		return false;
	}		
}
	
function carsearch()
{
	var srch = document.getElementById("carsrchbox").value;
	if (srch == "" || srch == null)
	{
		alert("Please enter the name of a car,\nvan, jeep, motorbike,\nor bicycle to proceed.");
		return false;
	}		
}

function srchfilter()
{
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("srchbox");
    filter = input.value.toUpperCase();
    ul = document.getElementById("schftrul");
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

