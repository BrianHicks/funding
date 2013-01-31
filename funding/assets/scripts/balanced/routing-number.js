function RoutingNumberModel(initial) {
    var self = this;

    self.value = ko.observable(initial || '');
    self.valid = ko.observable(function() {
        if (self.value() <= 5) return true;
        return false;
    });
    self.error = ko.observable('');
}
