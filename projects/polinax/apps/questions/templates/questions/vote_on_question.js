function vote_on_question(question_id, direction) {
    $.post('/questions/'+question_id + '/' + direction + 'vote/', function(data) {
        var jsonResult = eval('(' + data + ')');
        var new_score = jsonResult.score.score;
        $('#question_' + question_id + '_score').text(new_score);
    });
    if (direction == 'up') {
        $('#up_' + question_id).replaceWith('<a id="up_' + question_id + '" href="#" onclick="vote_on_question(' + question_id + ', \'clear\');"><img src="{{ MEDIA_URL }}up_mod.png"/>');
    }
    else { // clear
        $('#up_' + question_id).replaceWith('<a id="up_' + question_id + '" href="#" onclick="vote_on_question(' + question_id + ', \'up\');"><img src="{{ MEDIA_URL }}up_grey.png"/>');
    }
    return false;
}
        