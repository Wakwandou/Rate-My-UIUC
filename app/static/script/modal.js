$(document).ready(function () {
    $('#form').submit(function(event) {
        $.ajax({
            type: 'POST',
            url: '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'class': $('#review').find("#course").val(),
                'instructor': $('#review').find("#instructor").val(),
                'rating': $('#review').find("#rating").val(),
                'comment': $('#review').find("#comment").val(),
                'recommended': $('#review').find("#recommended").is(":checked"),
                'textbook': $('#review').find("#textbook").is(":checked")
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    })

    $('#edit').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const ReviewID = button.data('source') // Extract info from data-* attributes
        const username = button.data('username') // Extract info from data-* attributes
        const rating = button.data('rating') // Extract info from data-* attributes
        const comment = button.data('comment') // Extract info from data-* attributes
        const recommended = button.data('recommended') // Extract info from data-* attributes
        const textbook = button.data('textbook') // Extract info from data-* attributes
        const course = button.data('course') // Extract info from data-* attributes
        const instructor = button.data('instructor') // Extract info from data-* attributes
        
        $('#course').attr('ReviewID', ReviewID)

        const modal = $(this)
        modal.find("#course").val(course);
        modal.find("#rating").val(rating);
        modal.find("#comment").val(comment);
        modal.find("#recommended").val(recommended);
        modal.find("#textbook").val(textbook);
        modal.find("#instructor").val(instructor);
    })

    $('#edit-form').submit(function(event) {
        const review_id = $('#course').attr('ReviewID');
        $.ajax({
            type: 'POST',
            url: '/edit/' + review_id,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'class': $('#edit').find("#course").val(),
                'instructor': $('#edit').find("#instructor").val(),
                'rating': $('#edit').find("#rating").val(),
                'comment': $('#edit').find("#comment").val(),
                'recommended': $('#edit').find("#recommended").is(":checked"),
                'textbook': $('#edit').find("#textbook").is(":checked")
            }),
            success: function (res) {
                console.log(res.response);
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this);
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response);
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });
})