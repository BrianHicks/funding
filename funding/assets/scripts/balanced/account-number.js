function AccountNumberModel(initial) {
    var self = this;

    self.value = ko.observable(initial || '');
    self.error = ko.observable('');
    self.valid = ko.computed(function() {
        var value = self.value();
        if (value === '') return true;

        // balanced doesn't provide a helper method in this case, so we just
        // make sure it's all digits
        var valid = true;
        if (/\D/.exec(value) !== null) {
            valid = false;
            self.error('account number should be all digits');
        } // else if... for more validations
        return valid
    });
}
