#!/usr/bin/env python3
from flask import Flask
html = """
	<p id="transcript"></p>
	<script>
	recognition = new webkitSpeechRecognition();
	//var speechSynthesis = new webkitSpeechSynthesis();

	recognition.continuous = true;
	recognition.interimResults = false;

	var total_transcript = ''

	var first_char = /\S/;
	function capitalize(s) {
	  return s.replace(first_char, function(m) { return m.toUpperCase(); });
	}

	recognition.onerror = function(event) {
		console.log(event.error);
	}

	recognition.onresult = function(event) {
		var final_transcript = '';
		for (var i = event.resultIndex; i < event.results.length; ++i) {
			final_transcript += event.results[i][0].transcript;
			var u = new SpeechSynthesisUtterance();
			u.text = final_transcript;
			u.lang = 'en-US';
			speechSynthesis.speak(u);
			total_transcript += capitalize(final_transcript) + '<br>';
			document.getElementById("transcript").innerHTML = total_transcript;
		}
	};
	recognition.start()
</script>"""
app = Flask(__name__)
@app.route('/voice')
def default():
	return html
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)