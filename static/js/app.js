/**
 * AngularJS integration
 *
 */

'use strict';

//angular.module('swiftCollate', ['ngSanitize', 'ngWebSocket', 'ui.select'])
angular.module('swiftCollate', ['ngSanitize', 'ngWebSocket'])
    .factory('Stream', function($websocket, $rootScope, $q) {
	    // Open a WebSocket connection
	    var dataStream = $websocket('ws://santorini0.stage.lafayette.edu/collate/stream');
	    //var dataStream = $websocket('wss://santorini0.stage.lafayette.edu/collate/stream');

	    var data = "<span>No transcripts selected for collation</span>";

	    /*
	    var methods = {
		'data': data,
		listen: function() {
		    var deferred = $q.defer();

		    dataStream.onMessage(function(message) {
			    $rootScope.$apply( function() {
				    deferred.resolve(message);
				});
			});

		    return deferred.promise;
		}
	    };
	    */

	    /**
	     * Work-around for submitting requests to begin a collation
	     *
	     */
	    /*
	    $("#collate-form").submit(function(event) {
		    event.preventDefault();
		    
		    var transmitStream = new WebSocket('ws://santorini0.stage.lafayette.edu/collate/stream');
		    transmitStream.send( $(this).serializeArray() );
		});
	    */

	    var methods = {
		'data': data,
		listen: function(callback) {
		    dataStream.onMessage(function(message) {
			    $rootScope.$apply( function() {
				    callback.call(this, message);
				    //console.log(message);
				});
			})
		},
		send: function(message) {
		    dataStream.send( JSON.stringify(message) );
		}
	    };

	    return methods;
	})
    .controller('StreamController', function ($scope, Stream, $compile, $sce) {
	    $scope.Stream = Stream;
	    $scope.status = $sce.trustAsHtml($scope.Stream.data);
	    $scope.resetCollation = function(event) {
		$("#collation-content").empty();
	    };

	    Stream.listen(function(message) {
		    $scope.Stream.data = message.data;
		    $scope.status = $sce.trustAsHtml($scope.Stream.data);
		});
	    // @todo Refactor using a Promise instance
	    /*
	    Stream.listen().then(function(message) {
		    $scope.Stream.data = message.data;
		    $scope.status = $sce.trustAsHtml($scope.Stream.data);
		});
	    */

	    // @todo Deduplicate
	    $scope.requestCollation = function(event) {
		event.preventDefault();

		/*
		var params = { poem: $scope.poem,
			       baseText: $scope.baseText,
			       variants: $scope.variants,
			       tokenizer: $scope.tokenizer };
		*/
		// Work-around
		var variants = $scope.variants;
		if( !$('#variant-fields').hasClass('in') ) {
		    variants = $scope.allVariants;
		}

		var params = { poem: $scope.poem,
			       baseText: $scope.baseText,
			       variants: variants,
			       tokenizer: $scope.tokenizer };

		Stream.send(params);
	    };
	})
    .controller('FormController', function ($scope, Stream) {

	    /**
	     * To be integrated
	     *
	     */
	    $scope.poem = null;
	    $scope.baseText = null;
	    $scope.variants = {};

	    // By default, the variants should be populated
	    // @todo Populate this from a server endpoint
	    var variants = {};

	    $('input[type="checkbox"][name="variants"]').each(function(i) {
		    variants[$(this).val()] = $(this).val();
		    //$(this).prop('checked', true);
		});

	    $scope.allVariants = variants;

	    // Work-around

	    $scope.tokenizer = null;
	    
	    $scope.requestCollation = function(event) {
		event.preventDefault();

		/*
		var params = { poem: $scope.poem,
			       baseText: $scope.baseText,
			       variants: $scope.variants,
			       tokenizer: $scope.tokenizer };
		*/

		// Work-around
		var variants = $scope.variants;
		if( !$('#variant-fields').hasClass('in') ) {
		    variants = $scope.allVariants;
		}

		var params = { poem: $scope.poem,
			       baseText: $scope.baseText,
			       variants: variants,
			       tokenizer: $scope.tokenizer };
		Stream.send(params);
	    };
	    // @todo Deduplicate
	    $scope.resetCollation = function(event) {
		$("#collation-content").empty();
	    };
	});
