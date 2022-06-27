// With strict mode, you can not use undeclared variables
"use strict";

// On-page Load call with even listeners
    document.getElementById("mainbody").onload = function() {

        // initializing creds
        key_call()

        // Disable right click and inspect events
        disable_right_click()

        //initializing
        init()

        //Initializing color event listeners
        color_boxes_event_listners()

        // Even Listener for save button
        document.getElementById("sve").addEventListener("click",
            save,
            true
        );

        // Event Listener for clear button
        document.getElementById("clr").addEventListener("click",
            erase,
            true
        );

        // Event Listener for clear button
        document.getElementById("bck").addEventListener("click",
            ()=>{
                window.location.href="/navigation"
            },
            true
        );

        //Enable tooltips
        $(function () {
          $('[data-toggle="tooltip"]').tooltip()
        })

        // Console Clear after some time
        clear_console(500)

        // Dev message
        my_message()

    };

    // Cookie CSRF Functions
    function setCookie(name,value,days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }
    function getCookie(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }


    // sleep
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    // Async dev message
    async function my_message() {

        //sleep call
        await sleep(2000)

        //Custom message
        $(function() {
            var successOptions = {
                autoHideDelay: 20000,
                showAnimation: "fadeIn",
                hideAnimation: "fadeOut",
                hideDuration: 700,
                arrowShow: false,
                className: "success",
            };
            $.notify(`Hi this is Sanidhya Sharma :), This site is currently under development. \n Enjoy making real time Test predictions of single digits 0-9 on the canvas \n with sequential dense and CNN architecture \n Step 1 : Drawn on canvas \n Step 2 : Select the Architecture drop down \n Step 3 : Press Predict Button \n Step 4: Press clear button and retry :P`, successOptions);
        });

    }

    // Synchonus AJAX Getting the Credentials
    function key_call(){

       var rt = $.ajax({
            url: "/keyValuesCalls",
            type: 'GET',
            contentType: "application/json",
            dataType: 'json',
            cache: false,
            async: false,
        }).done( function(json) {

            // Storing keys
            var recieved_apiKey = json["x-api-key"]
            var recieved_tempKey = json["temp-key"]

            // Decrypting base64
            let org_apiKey = window.atob(recieved_apiKey)
            let org_tempKey = window.atob(recieved_tempKey)

            // Encrypt base64
            let apiKey = window.btoa(org_apiKey)
            let tempKey = window.btoa(org_tempKey)

            // let csrfToken = document.getElementsByName('csrf-token');
            // let csrfToken = document.head.querySelector("meta[name~=csrf-token][content]").content;
            let csrfToken = getCookie('csrf_token');

            // Calling global setup for AJAX Headers and CSRF
            Ajax_global_setup(apiKey, tempKey, csrfToken)

        })

        rt.fail( function(data) {
            // alert("Please Draw Something on the canvas")
            $.notify(`Please Draw Something on the canvas`, "error");

            // Notification Repeat Fix
            clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")
        });

    }

    // Global Ajax Setup
    function Ajax_global_setup(ApiKey, TempKey, CSRF= getCookie('csrf_token')) {
        // Setting global headers for AJAX request
        $.ajaxSetup({
            // CSRF Security
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", CSRF);
                }
            },
            mode: 'same-origin',
            // API Key
            headers: { 'x-api-key': ApiKey, 'temp-key': TempKey}
        });

        // Initialize Deep Learning model (It needs the Security)
        dl_initialization()
    };

    // Refresh CSRF and Keys
    function RefreshAjaxHeaders(ApiKey= getCookie('ak'), TempKey= getCookie('tk'), CSRF= getCookie('csrf_token')){

        // Setting global headers for AJAX request
        $.ajaxSetup({
            // CSRF Security
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", CSRF);
                }
            },
            mode: 'same-origin',
            // API Key
            headers: { 'x-api-key': ApiKey, 'temp-key': TempKey}
        });

    };

    // Disable the right click context menu, F12, cntrl+I to inspect and various other interactions
    function disable_right_click(){

        $(document).ready(function() {
            function disableSelection(e) {
                if (typeof e.onselectstart != "undefined") e.onselectstart = function() {
                    return false
                };
                else if (typeof e.style.MozUserSelect != "undefined") e.style.MozUserSelect = "none";
                else e.onmousedown = function() {
                    return false
                };
                e.style.cursor = "default"
            }
            window.onload = function() {
                disableSelection(document.body)
            };

            window.addEventListener("keydown", function(e) {
                if (e.ctrlKey && (e.which == 65 || e.which == 66 || e.which == 67 || e.which == 70 || e.which == 73 || e.which == 80 || e.which == 83 || e.which == 85 || e.which == 86)) {
                    e.preventDefault()
                }
            });
            document.keypress = function(e) {
                if (e.ctrlKey && (e.which == 65 || e.which == 66 || e.which == 70 || e.which == 67 || e.which == 73 || e.which == 80 || e.which == 83 || e.which == 85 || e.which == 86)) {}
                return false
            };

            document.onkeydown = function(e) {
                e = e || window.event;
                if (e.keyCode == 123 || e.keyCode == 18) {
                    return false
                }
            };

            document.oncontextmenu = function(e) {
                var t = e || window.event;
                var n = t.target || t.srcElement;
                if (n.nodeName != "A") return false
            };
            document.ondragstart = function() {
                return false
            };
        });

    }


    // clear console after few seconds Async
    function clear_console(ms) {

        // Async timeout
        function timeout(ms) {
            return new Promise(res => setTimeout(res, ms));
        }

        // Async function calling events after timeout
        async function fire_console_events() {
            await timeout(ms);
            console.clear()
        }

        // Calling the function
        fire_console_events()
    }


    // Variables for state
    var e = window.event

    var canvas, ctx, flag = false,
        prevX = 0,
        currX = 0,
        prevY = 0,
        currY = 0,
        dot_flag = false;

    var x = "black",
        y = 12.5;

    // Initialization call
    function init() {
        // Console log for checking running of the function
        // console.log("Running Init")

        document.getElementById("canvasimg").style.display = "none";

        // Initialization of canvas
        canvas = document.getElementById('can');
        ctx = canvas.getContext("2d");
        window.w = canvas.width;
        window.h = canvas.height;

        // Getting bounds of the rectangle
        // canvasBounds = canvas.getBoundingClientRect();

        // Even listeners with respect to each movement on canvas
        canvas.addEventListener("mousemove", function (e) {
            findxy('move', e)
        }, false);

        //touch
        canvas.addEventListener("touchmove", function (e) {
            findxy('move', e)
        }, false);

        canvas.addEventListener("mousedown", function (e) {
            findxy('down', e)
        }, false);

        // touch
        canvas.addEventListener("touchstart", function (e) {
            findxy('down', e)
        }, false);

        canvas.addEventListener("mouseup", function (e) {
            findxy('up', e)
        }, false);

        canvas.addEventListener("mouseout", function (e) {
            findxy('out', e)
        }, false);

        // touch
        canvas.addEventListener("touchend", function (e) {
            findxy('out', e)
        }, false);



        // Prevent scrolling when touching the canvas
        document.body.addEventListener("touchstart", function (e) {
          if (e.target == canvas) {
            e.preventDefault();
          }
        }, { passive: false });
        document.body.addEventListener("touchend", function (e) {
          if (e.target == canvas) {
            e.preventDefault();
          }
        }, { passive: false });
        document.body.addEventListener("touchmove", function (e) {
          if (e.target == canvas) {
            e.preventDefault();
          }
        }, { passive: false });


    }


    // Setting the active colour
    function active_color_box(obj) {

        // getting the active color clicked on by user
        let color = obj.id

        // Modified JSON for selected colors
        let color_lst = {"black":false, "green":false, "blue":false, "red":false, "white": false}

        // Defualt JSON for all colours
        // let color_lst = {"black":false, "green":false, "blue":false, "red":false, "yellow":false, "orange":false, "white": false}

        // Setting input as active "true"
        color_lst[color] = true

        // Assigning colours to active elements
        for(let x in color_lst) {
           if (color_lst[x] == true){
               document.getElementById(x).style.borderColor = "cyan";
               document.getElementById(x).style.transform = "scale(1.3)";
               document.getElementById(x).style.boxShadow = "5px 5px 7px grey";
           }else{
               document.getElementById(x).style.borderColor = "black";
               document.getElementById(x).style.transform = "scale(1)";
               document.getElementById(x).style.boxShadow = "0px 0px 0px grey";
           }
        }

    }

    // Initialization of event listeners for color boxes
    function color_boxes_event_listners(){

        // Even Listener for green button
        document.getElementById("green").addEventListener("click",
            function(){
                color(this)
                active_color_box(this)
            },
            true
        );

        // Even Listener for blue button
        document.getElementById("blue").addEventListener("click",
            function(){
                color(this)
                active_color_box(this)
            },
            true
        );

        // Even Listener for red button
        document.getElementById("red").addEventListener("click",
            function(){
                color(this)
                active_color_box(this)
            },
            true
        );
        // // Even Listener for yellow button
        // document.getElementById("yellow").addEventListener("click",
        //     function(){
    //          color(this)
        //     },
        //     true
        // );
        // // Even Listener for orange button
        // document.getElementById("orange").addEventListener("click",
        //     function(){
    //         color(this)
        //     },
        //     true
        // );
        // Even Listener for black button
        document.getElementById("black").addEventListener("click",
            function(){
                color(this)
                active_color_box(this)
            },
            true
        );
        // Even Listener for Eraser White button
        document.getElementById("white").addEventListener("click",
            function(){
                color(this)
                active_color_box(this)
            },
            true
        );

        // Defaulting to black colour
        document.getElementById("black").click();

    }

    // color selection
    function color(obj) {
        switch (obj.id) {
            case "green":
                x = "green";
                break;
            case "blue":
                x = "blue";
                break;
            case "red":
                x = "red";
                break;
            case "yellow":
                x = "yellow";
                break;
            case "orange":
                x = "orange";
                break;
            case "black":
                x = "black";
                break;
            case "white":
                x = "white";
                break;
        }
        if (x == "white") y = 14;
        else y = 12.5;

    }

    // Drawing the path
    function draw(e) {
        ctx.beginPath();

        // Accepting Mouse and Touch inputs ctx.lineTo(e.clientX, e.clientY);
        if (e.type == 'touchmove') {
            ctx.moveTo(e.touches[0].clientX, e.touches[0].clientY);
        }else {
            ctx.moveTo(prevX, prevY);
        }

        // Accepting Mouse and Touch inputs ctx.moveTo(e.clientX, e.clientY);
        if (e.type == 'touchmove') {
            ctx.lineTo(e.touches[0].clientX, e.touches[0].clientY);
        }else {
            ctx.lineTo(currX, currY);
        }

        ctx.strokeStyle = x;

        // ctx.lineWidth = y;  //commented due to issues with stroke

        const r = 10;               //marks the radius of the circle
        ctx.lineWidth = r * 2;
        ctx.lineCap = "round";

        ctx.stroke();
        ctx.closePath();
    }

    // Hiding extra notifications (BugFix)
    function clear_extra_notifications(class_name){
       // Hiding all the last elements
       let elements = document.getElementsByClassName(class_name)
       for (let i = 0; i < elements.length; i++) {
         if(i != 0) {
             elements[i].style.display ="none";
         }
        }
    }

    // Erase the drawing and deep learning prediction
    function erase() {
        // Flag to check if the canvas is empty or not
        let isEmptyCanvas = isCanvasBlank(canvas)

        if(!isEmptyCanvas) {

            //// Alert message to user
            // let m = confirm("Want to clear");
            // if (m) {
            //     ctx.clearRect(0, 0, window.w, window.h);
            //     document.getElementById("canvasimg").style.display = "none";
            //
            //     // Clear the deep learning h2 tag
            //     let headingDiv = document.getElementById("prediction_tag");
            //     headingDiv.innerHTML = "<H2> Deep Learning Predicts : </H2>";
            // }

            //add a new style 'foo'
            $.notify.addStyle('foo', {
              html:
                "<div>" +
                  "<div class='clearfix'>" +
                    "<div class='title' data-notify-html='title'/>" +
                    "<div class='buttons'>" +
                      "<button id='no_clear' class='no custom_btn_design'>&nbsp;<i class='gg_notify_close gg-close-o'></i></button>" +
                      "<button id='yes_clear' class='yes custom_btn_design'>&nbsp;<i class='gg_notify_check gg-check-o'></i></button>" +
                    "</div>" +
                  "</div>" +
                "</div>"
            });

            //listen for click events from this style
            // .notifyjs-foo-base .no --> #no_clear
            $(document).on('click', '#no_clear', function(e) {

                //programmatically trigger propogating hide event
                $(this).trigger('notify-hide');

                // Clear aborted
                $.notify(`Clear operation aborted !`, "warning");


                clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")

            });

            // .notifyjs-foo-base .yes --> #yes_clear
            $(document).on('click', '#yes_clear', function() {
                //show button text
                // alert($(this).text() + " clicked!");

                // Clearing the Canvas
                ctx.clearRect(0, 0, window.w, window.h);
                document.getElementById("canvasimg").style.display = "none";

                // Clear the deep learning h2 tag
                let headingDiv = document.getElementById("prediction_tag");
                headingDiv.innerHTML = "<H2> Deep Learning Predicts : </H2>";

                //hide notification
                $(this).trigger('notify-hide');

                // Cleared
                $.notify(`Cleared !`, "info");

                // Notification Repeat Fix
                clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")
            });

            $.notify({
              title: 'Would you like to clear the canvas ?',
              button: 'Yes'
            }, {
              style: 'foo',
              autoHide: false,
              clickToHide: false
            });

        }
        else{
            //// Alerts
            // alert("Looks like the canvas is already clear !")
            $.notify(`Looks like the canvas is already clear !`, "warning");

            // Notification Repeat Fix
            clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")
        }

    }

    // This function is used to make a copy of reduced canvas image
     function resize_image(width, height, orignal_image){
          // create a new canvas
          let c = document.createElement('canvas');
          // set its width & height to the required ones
          c.width = width;
          c.height = height;
          // draw our canvas to the new one
          c.getContext('2d').drawImage(orignal_image, 0,0,orignal_image.width, orignal_image.height, 0,0, width, height);
          // return the resized canvas dataURL
          return c.toDataURL();
      }

      // Function to check if the canvas is empty or !empty (False : Not Empty, True : Empty)
     function isCanvasBlank(canvas) {
          const context = canvas.getContext('2d');

          const pixelBuffer = new Uint32Array(
            context.getImageData(0, 0, canvas.width, canvas.height).data.buffer
          );

          return !pixelBuffer.some(color => color !== 0);
     }

    // Saving the image in 28 * 28 size
    function save() {
        // Flag to check if the canvas is empty or not
        let isEmptyCanvas = isCanvasBlank(canvas)

        if(!isEmptyCanvas) {
            document.getElementById("canvasimg").style.border = "2px solid";

            // Saving image without resize
            // let dataURL = canvas.toDataURL();

            // Save image with resize and store the dataURL
            let dataURL = resize_image(28, 28, canvas);

            document.getElementById("canvasimg").src = dataURL;
            document.getElementById("canvasimg").style.display = "inline";

            // requesting values selected for architecture of deep learning
            let requested_architecture_select = document.getElementById("deep_learning_infra");
            let requested_architecture = requested_architecture_select.value;

            // Posting the saved dataURL to backend via AJAX call
            save_post(dataURL, requested_architecture);
        }
        else{
            // alert("Please Draw Something on the canvas")
            $.notify(`Please Draw Something on the canvas`, "error");

            // Notification Repeat Fix
            clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")
        }
    }

    // Sending the image to the backend and recieve the responce
    function save_post(dataURL, requested_architecture){

        // JSON for image in base 64 encode
        let image_post = {
            "image_base64" : dataURL,
            "architecture" : requested_architecture
        }

        // Refreshing headers
        RefreshAjaxHeaders()

        // AJAX POST call
        $.ajax({
          type: "POST",
          url: "/result",
          data: JSON.stringify(image_post),
          contentType: "application/json",
          cache: false,
          async: false,
          dataType: 'json',
            // Success
            success: function(response) {

                // Positive response message
                // alert("Successfully Saved the image ")
                // console.log(response.data)

                // Recieving the Deep Learning response and adding it to h2 tag
                let headingDiv = document.getElementById("prediction_tag");
                // headingDiv.innerHTML = "<H2> Deep Learning Predicts : "+response.data+"</H2>";

                if(response.data == "No Architecture Selected"){
                    headingDiv.innerHTML = "<h4> Deep Learning Predicts :<br><br><span><i class=\"canvas_icon_bot gg-bot\"></i></span></h4><br><div class='circle'><h2 class='responce_dl'>" + response.data + "<h2></div>";
                    $.notify(`Please select the model architecture !`, "warning");

                    // Focus on the element and blink
                    document.getElementById("deep_learning_infra").focus();
                    document.getElementById("deep_learning_infra").classList.add("blink_me")

                    setTimeout( () => {document.getElementById("deep_learning_infra").classList.remove("blink_me")} , 5000)

                    // Notification Repeat Fix
                    clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")

                }
                // Auth Error
                else if(response.code == "401"){

                    window.location = response.redirect_url;

                }else {
                    headingDiv.innerHTML = "<h4> Deep Learning Predicts :<br><br><span><i class=\"canvas_icon_bot gg-bot\"></i></span></h4><br><div class='circle'><h1 class='responce_dl'>" + response.data + "<h1></div>";
                    $.notify(`Prediction Successful`, "success");

                    // Notification Repeat Fix
                    clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")
                }

            },
            // Fail
            error: function (jqXHR, exception ,response) {
                let msg = '';
                if (jqXHR.status === 0) {
                    msg = 'Not connect.\n Verify Network.';
                } else if (jqXHR.status == 404) {
                    msg = 'Requested page not found. [404]';
                } else if (jqXHR.status == 500) {
                    msg = 'Internal Server Error [500].';
                } else if (jqXHR.status == 400) {
                    msg = 'Bad Request';
                } else if (jqXHR.status == 403) {
                    msg = 'Forbidden Request';
                } else if (exception === 'parsererror') {
                    msg = 'Requested JSON parse failed.';
                } else if (exception === 'timeout') {
                    msg = 'Time out error.';
                } else if (exception === 'abort') {
                    msg = 'Ajax request aborted.';
                } else {
                    msg = 'Uncaught Error.\n' + jqXHR.responseText;
                }

                //Destroy the saved element due to it not being saved in backend
                let elem = document.getElementById("canvasimg");
                elem.setAttribute('src', '');
                elem.style.display = 'none';

                // alert(msg)
                // alert("Some Error")

                // Check if status is 400 for CSRF token to apply custom message
                if(jqXHR.responseJSON.code == "403"){

                    window.location = jqXHR.responseJSON.redirect_url;

                    //Custom message with a refresh button
                    $(function() {

                        //add a new style 'foo'
                        $.notify.addStyle('foo', {
                          html:
                            "<div>" +
                              "<div class='clearfix'>" +
                                "<div class='title' data-notify-html='title'/>" +
                                "<div class='buttons' align='center'>" +
                                  "<button id='Refresh' class='Refresh custom_btn_design'>&nbsp;<i class='gg-redo'></i></button>" +
                                "</div>" +
                              "</div>" +
                            "</div>"
                        });

                        //listen for click events from this style
                        // .notifyjs-foo-base .Refresh --> #Refresh
                        $(document).on('click', '#Refresh', function(e) {

                            //programmatically trigger propogating hide event
                            $(this).trigger('notify-hide');

                            // Clear aborted
                            $.notify(`Refreshing !`, "warning");

                            clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")

                            // Refresh
                            location.reload();
                        });

                        $.notify({
                          title: "CSRF Token Mismatch \n Tokens Expired Please Refresh !.",
                          button: 'Yes'
                        }, {
                          style: 'foo',
                          autoHide: false,
                          clickToHide: false,
                          autoHideDelay: 10000,
                          showAnimation: "fadeIn",
                          hideAnimation: "fadeOut",
                          hideDuration: 700,
                          arrowShow: false,
                          className: "success",
                        });

                    });

                }else{
                    $.notify(`Hmm Somthings not Fine here \n Looks like there is : ${msg}`, "error");
                }

                // $.notify(`Hmm Somthings not Fine here \n Looks like there is : ${msg}`, "error");

                // Notification Repeat Fix
                clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")
            },
        });
    }


    // Posting to the backend endpoint for initialaization of deep learning models
    function dl_initialization(){

        // AJAX POST call
        $.ajax({
          type: "POST",
          url: "/dl_initialization",
          data: JSON.stringify(""),
          contentType: "application/json",
          cache: false,
          async: false,
          dataType: 'json',

            // Success
            success: function(response) {

                // Positive response message
                // console.log(response)

                if(response.success){
                    $.notify(`${response.data}`, "success");

                    // Notification Repeat Fix
                    clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")

                }
                // Auth Error
                else if(response.code == "401"){

                    window.location = response.redirect_url;

                }else{

                    $.notify(`${response.data}`, "error");

                    // Notification Repeat Fix
                    clear_extra_notifications("notifyjs-wrapper notifyjs-hidable")
                }

            },
            // Fail
            // error: function (jqXHR, exception) {
            //     let msg = '';
            //     if (jqXHR.status === 0) {
            //         msg = 'Not connect.\n Verify Network.';
            //     } else if (jqXHR.status == 404) {
            //         msg = 'Requested page not found. [404]';
            //     } else if (jqXHR.status == 500) {
            //         msg = 'Internal Server Error [500].';
            //     } else if (exception === 'parsererror') {
            //         msg = 'Requested JSON parse failed.';
            //     } else if (exception === 'timeout') {
            //         msg = 'Time out error.';
            //     } else if (exception === 'abort') {
            //         msg = 'Ajax request aborted.';
            //     } else {
            //         msg = 'Uncaught Error.\n' + jqXHR.responseText;
            //     }
            //
            //     //Destroy the saved element due to it not being saved in backend
            //     let elem = document.getElementById("canvasimg");
            //     elem.setAttribute('src', '');
            //     elem.style.display = 'none';
            //
            //     // alert(msg)
            //     alert("Some Error")
            // },
        });
    }


    // Function responsible for drawing with respect to event listener call
    function findxy(res, e) {

        // Getting body element
        let scroll_lock = document.getElementById("mainbody")

        if (res == 'down') {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;

            flag = true;
            dot_flag = true;

            if (dot_flag) {
                ctx.beginPath();
                ctx.fillStyle = x;
                ctx.fillRect(currX, currY, 2, 2);
                ctx.closePath();
                dot_flag = false;
            }
        }
        if (res == 'up' || res == "out") {
            flag = false;
        }
        if (res == 'move') {

            if (flag) {
                prevX = currX;
                prevY = currY;
                currX = e.clientX - canvas.offsetLeft;
                currY = e.clientY - canvas.offsetTop;

                draw(e);

                // Scroll lock when drawing
                // scroll_lock.style.overflow = "hidden"
            }

        }else
            {
                // Scroll not locked
                // scroll_lock.style.overflow = "visible"
            }
    }