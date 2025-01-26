document.addEventListener('DOMContentLoaded', function () {
  // Get references to the spinner and feedback form
  const spinner_ = document.getElementById('spinner');
  const generate_tour = document.getElementById('generate-tour');
  const Sub_btn = document.getElementById('Submit_btn');

  // Add event listener to the form submission
  if (generate_tour){
    generate_tour.addEventListener('submit', function (e) {
        // Show the spinner by adding the 'show' class
        spinner_.classList.add('show');
  
        // Disable the button to prevent multiple submissions
        Sub_btn.disabled = true;
    });
  }
});


document.addEventListener('DOMContentLoaded', function () {
  // Get references to the spinner and feedback form
  const spinner = document.getElementById('spinner');
  const Form_ = document.getElementById('Form');
  const Submit_btn = document.getElementById('Submit_btn');

  // Add event listener to the form submission
  if (Form_){
    Form_.addEventListener('submit', function (e) {
        // Show the spinner by adding the 'show' class
        spinner.classList.add('show');
  
        // Disable the button to prevent multiple submissions
        Submit_btn.disabled = true;
    });
  }
});


// For auto Scrolling in generate plan or forts found
document.addEventListener("DOMContentLoaded", function() {
  const forts_found = document.getElementById("forts_found"); 
  const generatedplan = document.getElementById("generatedplan");
  const alert_ = document.getElementById("alert");

  if (forts_found) {
    forts_found.scrollIntoView({ behavior: "smooth" });
  }

  if (generatedplan) {
    // generatedplan.scrollIntoView({ behavior: "smooth" });
    generatedplan.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  if (alert_){
    alert_.scrollIntoView({ behavior: "smooth" });
  }
});



document.addEventListener("DOMContentLoaded", function () {
    // Parse URL parameters
    const params = new URLSearchParams(window.location.search);
    const scrollId = params.get("scroll_id");

    if (scrollId) {
        const element = document.getElementById(scrollId);
        if (element) {
            element.scrollIntoView({ behavior: "smooth" });
        }
    }
});



function showDirections(button) {
  // Get the value of the data-item attribute
  const itemData = button.getAttribute('data-item');

  // Remove parentheses and single quotes
  const cleanedInput = itemData.replace(/[()']/g, "");

  // Split the string by the comma separating the coordinate pairs
  const coordinatePairs = cleanedInput.split(", ");

  // Further split each coordinate pair into latitude and longitude
  const coordinates = coordinatePairs.map(pair => pair.split(","));

  // Access each coordinate
  const [lat1, lon1] = coordinates[0];
  const [lat2, lon2] = coordinates[1];

  // Output the results
  // console.log("First Coordinate:", { latitude: lat1, longitude: lon1 });
  // console.log("Second Coordinate:", { latitude: lat2, longitude: lon2 });

  // Construct the Google Maps URL
  // "https://www.google.com/maps/dir/'19.2454,73.1186'/'19.2962,72.8883'/" 
  var mapsUrl = "https://www.google.com/maps/dir/" + lat1 + "," + lon1 + "/" + lat2 + "," + lon2 + "/"

  // Open Google Maps in a new tab
  window.open(mapsUrl, "_blank");
}


(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();



    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });
    
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });

})(jQuery);




$(document).ready(function() {
    $("#get-user-location").click(function() {
        navigator.geolocation.getCurrentPosition(function(position) {
            let latitude = position.coords.latitude;
            let longitude = position.coords.longitude;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Show loading indicator
            // $('#user-loc-animation').show();
            $('#spinner').addClass('show');

            // Send coordinates to djabgo using AJAX 
            $.ajax({
                url: "send-coordinates/",
                type: "POST",
                headers: {
                  'X-CSRFToken': csrfToken  // Add the CSRF token here
                },
                data: {
                    latitude: latitude,
                    longitude: longitude,
                },
                dataType : "json",
                success: function(response) {
                      console.log(response.success_msg);

                      $('#spinner').removeClass('show');
                }
            });
        }, function(error) {
            console.error("Error getting geolocation:", error);
            alert("Error getting your location. Please check your browser settings.");
        });
    });
});





var multipleCardCarousel = document.querySelector("#carouselExampleControls");
if(multipleCardCarousel){
    if (window.matchMedia("(min-width: 768px)").matches) {
        var carousel = new bootstrap.Carousel(multipleCardCarousel, {
          interval: false,
        });
        var carouselWidth = $(".carousel-inner")[0].scrollWidth;
        var cardWidth = $(".carousel-item").width();
        var scrollPosition = 0;
        $("#carouselExampleControls .carousel-control-next").on("click", function () {
          if (scrollPosition < carouselWidth - cardWidth * 4) {
            scrollPosition += cardWidth;
            $("#carouselExampleControls .carousel-inner").animate(
              { scrollLeft: scrollPosition },
              600
            );
          }
        });
        $("#carouselExampleControls .carousel-control-prev").on("click", function () {
          if (scrollPosition > 0) {
            scrollPosition -= cardWidth;
            $("#carouselExampleControls .carousel-inner").animate(
              { scrollLeft: scrollPosition },
              600
            );
          }
        });
    } else {
        $(multipleCardCarousel).addClass("slide");
    }
}


