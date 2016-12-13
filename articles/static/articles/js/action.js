/**
 * Created by Valeriia on 13.12.2016.
 */
$(document).ready(function(){
    $('.btn-crud').hide();
    $('.comment-col .form-crud').hide();

    $('#comment_input').on('click', function(){
        $(this).height(150);
        $(this).attr('placeholder', '');
});

    $('.comment-col').on('mouseenter', function () {
        btns = $(this).find('.btn-crud');
        btns.show();
        comment_col = $(this);
        btns.first().on('click', function () {
            comment_col.find('.form-crud:last-child').submit();
        });
        btns.last().on('click', function(){
            comment_text = comment_col.find('.comment-text').hide();
            comment_update = comment_col.find('.form-crud').first();
            comment_update.find('button:last-child').on('click', function(){
                comment_update.find('textarea').val(comment_text.text());
                comment_update.hide();
                comment_text.show();
            });
            comment_update.show();
        });

    });

    $('.comment-col').on('mouseleave', function(){
        $(this).find('.btn-crud').hide();
    });

});
