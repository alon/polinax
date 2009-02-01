        function vote_on_answer(a_id, direction) {
            $.post('/answers/' + a_id + '/' + direction + 'vote/', function(data) {
                var jsonResult = eval('(' + data + ')');
                var new_score = jsonResult.score.score;
                $('#a_' + a_id + '_score').text(new_score);
            });
            if (direction == 'up') {
                $('#up_' + a_id).replaceWith('<a id="up_' + a_id + '" href="#" onclick="return false;"><img src="{{ MEDIA_URL }}up_mod.png"/>');
                $('#down_' + a_id).replaceWith('<a id="down_' + a_id + '" href="#" onclick="vote_on_answer(' + a_id + ', \'clear\'); return false;"><img src="{{ MEDIA_URL }}down_grey.png"/>');
            }
            else if (direction == 'down') {
                $('#up_' + a_id).replaceWith('<a id="up_' + a_id + '" href="#" onclick="vote_on_answer(' + a_id + ', \'clear\'); return false;"><img src="{{ MEDIA_URL }}up_grey.png"/>');
                $('#down_' + a_id).replaceWith('<a id="down_' + a_id + '" href="#" onclick="return false;"><img src="{{ MEDIA_URL }}down_mod.png"/>');
            }
            else { // clear
                $('#up_' + a_id).replaceWith('<a id="up_' + a_id + '" href="#" onclick="vote_on_answer(' + a_id + ', \'up\'); return false;"><img src="{{ MEDIA_URL }}up_grey.png"/>');
                $('#down_' + a_id).replaceWith('<a id="down_' + a_id + '" href="#" onclick="vote_on_answer(' + a_id + ', \'down\'); return false;"><img src="{{ MEDIA_URL }}down_grey.png"/>');
            }
            return false;
        }
