'use strict'
app.factory('Facebook', ["$q", "$state", "$rootScope",
    function($q, $state, $rootScope) {

    // since we are resolving a thirdparty response,
    // we need to do so in $apply
    var resolve = function(errval, retval, deferred) {
        $rootScope.$apply(function() {
            if (errval) {
                deferred.reject(errval);
            } else {
                retval.connected = true;
                deferred.resolve(retval);
            }
        });
    }

    var _login = function() {
        var deferred = $q.defer();
        //first check if we already have logged in
        FB.getLoginStatus(function(response) {
            if (response.status === 'connected') {
                // the user is logged in and has authenticated your
                // app
                deferred.resolve(response);
            } else {
                // the user is logged in to Facebook,
                // but has not authenticated your app
                FB.login(function(response) {
                    if (response.authResponse) {
                        // redirect the user to the same page let him authorise the application
                        resolve(null, response, deferred);
                    } else {
                        //redirect user to same page and echo failure to log in
                        resolve(response.error, null, deferred);
                    }
                });
            }
        });

        return deferred.promise;
    }

    return {
        login: _login,
        // getPhoto: _getPhoto,
    };
}
]);
