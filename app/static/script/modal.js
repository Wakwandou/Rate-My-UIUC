$(document).ready(function () {
    $('#submit').click(function () {
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

    $('#submit-edit').click(function () {
        const review_id = $('#task-form-display').attr('ReviewID');
        // console.log($('#task-modal').find('.form-group').val())
        $.ajax({
            type: 'POST',
            url: '/edit/' + review_id,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'class': $('#task-modal').find("#class").val(),
                'rating': $('#task-modal').find("#rating").val(),
                'comment': $('#task-modal').find("#comment").val(),
                'recommended': $('#task-modal').find("#recommended").is(":checked"),
                'textbook': $('#task-modal').find("#textbook").is(":checked"),
                'instructor': $('#task-modal').find("#instructor").val()
            }),
            success: function (res) {
                console.log(res.response)
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

});


// $(document).ready(function () {
//     // example: https://getbootstrap.com/docs/4.2/components/modal/
//     // show modal
//     $('#addReview').on('show.bs.modal', function (event) {
//         const button = $(event.relatedTarget) // Button that triggered the modal
//         const ReviewID = button.data('source') // Extract info from data-* attributes
//         const username = button.data('username') // Extract info from data-* attributes
//         const rating = button.data('rating') // Extract info from data-* attributes
//         const comment = button.data('comment') // Extract info from data-* attributes
//         const recommended = button.data('recommended') // Extract info from data-* attributes
//         const textbook = button.data('textbook') // Extract info from data-* attributes
//         const course = button.data('course') // Extract info from data-* attributes
//         const instructor = button.data('instructor') // Extract info from data-* attributes

//         const modal = $(this)
//         if (!ReviewID) {
//             modal.find('.modal-title').text(ReviewID)
//             $('#task-form-display').removeAttr('ReviewID')
//         } else {
//             modal.find('.modal-title').text('Edit Review on ' + ReviewID)
//             $('#task-form-display').attr('ReviewID', ReviewID)
//         }

//         if (course) {
//             modal.find("#class").val(course);
//             modal.find("#rating").val(rating);
//             modal.find("#comment").val(comment);
//             modal.find("#recommended").val(recommended);
//             modal.find("#textbook").val(textbook);
//             modal.find("#instructor").val(instructor);
//         } else {
//             modal.find('.form-control').val('');
//         }
//     })

//     $('#submit-task').click(function () {
//         const review_id = $('#task-form-display').attr('ReviewID');
//         // console.log($('#task-modal').find('.form-group').val())
//         $.ajax({
//             type: 'POST',
//             url: review_id ? '/edit/' + review_id : '/create',
//             contentType: 'application/json;charset=UTF-8',
//             data: JSON.stringify({
//                 'class': $('#task-modal').find("#class").val(),
//                 'rating': $('#task-modal').find("#rating").val(),
//                 'comment': $('#task-modal').find("#comment").val(),
//                 'recommended': $('#task-modal').find("#recommended").is(":checked"),
//                 'textbook': $('#task-modal').find("#textbook").is(":checked"),
//                 'instructor': $('#task-modal').find("#instructor").val()
//             }),
//             success: function (res) {
//                 console.log(res.response)
//                 location.reload();
//             },
//             error: function () {
//                 console.log('Error');
//             }
//         });
//     });

//     $('.remove').click(function () {
//         const remove = $(this);
//         $.ajax({
//             type: 'POST',
//             url: '/delete/' + remove.data('source'),
//             success: function (res) {
//                 console.log(res.response);
//                 location.reload();
//             },
//             error: function () {
//                 console.log('Error');
//             }
//         });
//     });
// });