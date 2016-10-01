/*
 * View model for OctoPrint-Vlcd
 *
 * Author: Fredrik Markstrom
 * License: AGPLv3
 */
$(function() {
    function VlcdViewModel(parameters) {
        var self = this;
	var text = "";

	self.vlcd_text = ko.observable();
	
	self.onStartupComplete = function() {
	    $("#vlcdarea").keydown(function(event) {
		var handled = true
		switch(event.which) {
		case  13: // enter
		    self.bclk();
		    break;
		case 82:  // r
		    self.brefresh();
		    break;
		case 37: // up
		    self.bup1();
		    break;
		case 39: // down
		    self.bdn1();
		    break;
		case 33: // pg-up
		    self.bup10();
		    break;
		case 34: // pg-dn
		    self.bdn10();
		    break;
		default:
		    handled = false;
		}
		if(handled)
		    event.preventDefault();
	    });
	}
	self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "vlcd") {
		return;
            }
	    if(data.lineno == 0)
		self.text = "";
	    self.text = self.text + data.vlcdtext + "\n";
            self.vlcd_text(self.text)
	};
	self.send = function(move, click) {
	    self.text = "";
	    console.log("Send: " + move  + ":" + click);
	    $.ajax({
                type: "GET",
                url: API_BASEURL + "plugin/vlcd?move=" + move + "&click=" + click
            });
	}
	self.bup100 = function() { self.send(-100, 0); }
	self.bup10  = function() { self.send(-10, 0); }	
	self.bup1   = function() { self.send(-1, 0); }
	self.bclk   = function() { self.send(0, 1); }
	self.bdn1   = function() { self.send(1, 0); }
	self.bdn10  = function() { self.send(10, 0); }
	self.bdn100 = function() { self.send(100, 0); }
	self.brefresh = function() { self.send(0, 0); }
    }
    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        VlcdViewModel,
        [],
        [ "#vlcdarea", "#buttons"]
    ]);
});
