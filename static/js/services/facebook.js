app.factory('Facebook', ["$q", "$state", "$rootScope",
    function($q, $state, $rootScope) {

    // use $apply to resolve to a third party service.
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

    var login = function() {
        var deferred = $q.defer();
        // check for logged in user.
        FB.getLoginStatus(function(response) {
            if (response.status === 'connected') {
                // logged in fb user
                deferred.resolve(response);
            } else {
                // authenticate a fb logged-in user on the app using a dialog.
                FB.login(function(response) {
                    if (response.authResponse) {
                        // redirect to let user authorize app
                        resolve(null, response, deferred);
                    } else {
                        // redirect user to show failure of logging in.
                        resolve(response.error, null, deferred);
                    }
                });
            }
        });

        return deferred.promise;
    };

    return {
        login: login
    };
}
]);
