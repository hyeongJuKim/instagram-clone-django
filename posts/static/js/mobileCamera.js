$(document).ready(function(){

  $('.take-picture').on('change',handleImgFileSelect);
  function handleImgFileSelect(event) {
    // Get a reference to the taken picture or chosen file
    var files = event.target.files,
        file;

    var id = $(this).attr('id');
    var idx = id.replace("take-picture","");
    var showPicture = document.getElementById('show-picture'+idx);

    if (files && files.length > 0) {
      file = files[0];
      try {
        // Get window.URL object
        var URL = window.URL || window.webkitURL;
        
        // Create ObjectURL
        var imgURL = URL.createObjectURL(file);
        
        // Set img src to ObjectURL
        showPicture.src = imgURL;

        // Revoke ObjectURL after imagehas loaded
        showPicture.onload = function() {
            URL.revokeObjectURL(imgURL);  
        };
      }
      catch (e) {
        try {
            // Fallback if createObjectURL is not supported
            var fileReader = new FileReader();
            fileReader.onload = function (event) {
              showPicture.src = event.target.result;
            };
            fileReader.readAsDataURL(file);
        }
        catch (e) {
          // Display error message
          var error = document.querySelector("#error");
          if (error) {
              error.innerHTML = "Neither createObjectURL or FileReader are supported";
          }
        }
      }
    }
    
  }

  // 첨부파일 삭제. no image로 교체. 첨부파일YN = N. N일경우 업로드 X
  $('.delete-picture').on('click',function() {
    var idx = $(this).attr('id').replace("delete-picture","");
    var takePicture = $('#take-picture'+idx);
    var showPicture = $('#show-picture'+idx);
    var agent = navigator.userAgent.toLowerCase();

    if ( (navigator.appName == 'Netscape' && navigator.userAgent.search('Trident') != -1) || (agent.indexOf("msie") != -1) ){
      // ie 일때 input[type=file] init.
      takePicture.replaceWith( $("#excelFile").clone(true) );
      // showPicture.attr("src","img/noImg.jpg"); //about:blank대신 noimage.jpg로 대체
    } else {
      //other browser 일때 input[type=file] init.
      takePicture.val("");
      // showPicture.attr("src","img/noImg.jpg"); //about:blank대신 noimage.jpg로 대체
    }
  });

});