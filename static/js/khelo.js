// <------------ Group-Team Section-------------->
console.log("script loaded");
// In the window that opens the new window
// call this function in on_click of each particular teams
function third_party_signup(event_id,team_id){
	var user_token = localStorage.getItem("user_token");
	if (user_token == null || user_token == 'undefined') {
		var popup = window.open("http://khelo.club/signup?event_id="+event_id+"&team_id="+team_id+"&source=mdfaofficial.com",'popUpWindow','height=500,width=500,left=100,top=100');
	}else{
		
		$.ajax({
		    url: "http://api.khelo.club/api/v1/events/"+event_id+"/team/"+team_id+"/get_team_players",
		    headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Token ' + user_token
            },
		    type: "GET",
		    dataType : "json",
		})
		  .done(function( json ) {
		  alert(JSON.stringify(json));
		  	// <<<<<<<<<< write the code to show a popup with Team players list with stats.>>>>>>>>>>>>>
		  })
		  .fail(function( xhr, status, errorThrown ) {
		    alert( "Sorry, there was a problem!" );
		    console.log( "Error: " + errorThrown );
		    console.log( "Status: " + status );
		  });
	}
}

window.addEventListener("message", receiveMessage, false);

function receiveMessage(event)
{
    alert("User Token: "+event.data.user_token);
	localStorage.setItem("user_token", event.data.user_token);
}


// <------------ Fixture Section-------------->

// call this function in on_click of each fixtures
function third_party_signup_fixture(event_id,fixture_id){
    var user_token = localStorage.getItem("user_token");
	if (user_token == null || user_token == 'undefined') {
		var popup = window.open("http://khelo.club/signup?event_id="+event_id+"&fixture_id="+fixture_id+"&source=mdfaofficial.com",'popUpWindow','height=500,width=500,left=100,top=100');
	}else{
		$.ajax({
		    url: "http://api.khelo.club/api/v1/fixture/"+fixture_id+"/get_fixture_players",
		    headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Token ' + user_token
            },
		    type: "GET",
		    dataType : "json",
		})
		  .done(function( json ) {
		  alert(JSON.stringify(json))
		  	// <<<<<<<<<< write the code to show a popup with Team players list with stats.>>>>>>>>>>>>>
		  })
		  .fail(function( xhr, status, errorThrown ) {
		    alert( "Sorry, there was a problem!" );
		    console.log( "Error: " + errorThrown );
		    console.log( "Status: " + status );
		  });
	}
}
