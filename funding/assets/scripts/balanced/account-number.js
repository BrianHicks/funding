function AccountNumberModel(initial) {
    var self = this;

    self.value = ko.observable(initial || '');
    self.valid = ko.computed(function() {
        var value = self.value();
        if (value.length <= 5) return true;

        // balanced doesn't provide a helper method in this case, so we just
        // make sure it's all digits
        return /\D/.exec(value) === null;
    });
}
