'use strict'

app.factory('RestService', function($resource) {
    return {
        Image: $resource('api/photo/', {}, {
            getImage: {
                method: 'GET', isArray: false
            }
        }, { stripTrailingSlashes: false }),
        ModifyImage: $resource('api/edit_photo/', {}, {
            deleteImage: {
                method: 'DELETE'
            },
            getImageEffects: {
                method: 'GET',
                isArray: false
            }
        }, { stripTrailingSlashes: false }),
    }
})

app.factory('Toast', function($mdToast) {
    var last = {
        bottom: false, top: true,
        left: false, right: true
    };
    var toastPosition = angular.extend({},last);
    var sanitizePosition = function () {
        var current = toastPosition;
        if ( current.bottom && last.top ) current.top = false;
        if ( current.top && last.bottom ) current.bottom = false;
        if ( current.right && last.left ) current.left = false;
        if ( current.left && last.right ) current.right = false;
        last = angular.extend({},current);
    }
    var getToastPosition = function () {
        sanitizePosition();
        return Object.keys(toastPosition)
          .filter(function(pos) { return toastPosition[pos]; })
          .join(' ');
    };

    return {
        show: function(message) {
            $mdToast.show(
            $mdToast.simple()
                .textContent(message)
                .position(getToastPosition())
                .hideDelay(2000)
            );
        }
    }
});

app.factory('Menu', function($mdSidenav, $timeout, Toast) {
    return {
        toggle: function(side) {
            return buildDelayedToggler(side);
        }
    }
    /**
     * Supplies a function that will continue to operate until the
     * time is up.
     */
    function debounce(func, wait, context) {
      var timer;
      return function debounced() {
        var context,
            args = Array.prototype.slice.call(arguments);
        $timeout.cancel(timer);
        timer = $timeout(function() {
          timer = undefined;
          func.apply(context, args);
        }, wait || 10);
      };
    }
    /**
     * Build handler to open/close a SideNav; when animation finishes
     * report completion in console
     */
    function buildDelayedToggler(navID) {
      return debounce(function() {
        $mdSidenav(navID)
          .toggle()
          .then(function () {});
      }, 200);
    }
});
