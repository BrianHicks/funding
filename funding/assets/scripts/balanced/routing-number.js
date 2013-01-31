function RoutingNumberModel(initial) {
    var self = this;

    self.value = ko.observable(initial || '');
    self.valid = ko.computed(function() {
        var value = self.value();
        if (value.length <= 5) return true;
        return balanced.bankAccount.validateRoutingNumber(value);
    });
    self.error = ko.observable('');
}
