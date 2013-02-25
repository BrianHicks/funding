function RoutingNumberModel(initial) {
    var self = this;

    self.value = ko.observable(initial || '');
    self.valid = ko.computed(function() {
        var value = self.value();
        if (value.length <= 5) return true;
        return balanced.bankAccount.validateRoutingNumber(value);
    });
}

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

function NameModel(initial) {
    var self = this;

    self.value = ko.observable(initial || '');
    self.error = ko.observable('');
    self.valid = ko.computed(function() {
        var value = self.value();
        if (value.length < 2) return true;
        if (value.length < 5) {
            self.error('Please enter the full name shown on the account');
            return false;
        }
        self.error('');
        return true;
    });
}

function TypeModel() {
    var self = this;

    self.value = ko.observable();
    self.changed = false;
    self.error = ko.observable('');
    self.valid = ko.computed(function() {
        var value = self.value();
        if (!value) {
            self.error('Please select an account type');
            return false;
        }
        return true;
    });
}

function BankAccountModel() {
    var self = this;

    self.showGeneralError = ko.observable(false);
    self.generalError = ko.observable('Please correct the errors before continuing.');

    self.balancedUri = ko.observable();

    self.routingNumber = new RoutingNumberModel('321174851');
    self.accountNumber = new AccountNumberModel('123456');
    self.name = new NameModel('Brian Hicks');
    self.type = new TypeModel('checking');

    self.valid = ko.computed(function() {
        return self.routingNumber.valid()
            && self.accountNumber.valid()
            && self.name.valid()
            && self.type.valid()
            && self.routingNumber.value()
            && self.accountNumber.value()
            && self.name.value()
            && self.type.value();
    });

    self.responseHandler = function(response) {
        switch(response.status) {
            case 400: // missing or invalid field
                self.showGeneralError(true);
                self.generalError('Missing or invalid field - please check your entry and try again.');
                return false;
                break;
            case 402:
                self.showGeneralError(true);
                self.generalError('Failed to authorize your card - please check your entry and try again.');
                return false;
                break;
            case 404: // marketplace URI is incorrect
                self.showGeneralError(true);
                self.generalError('Something went wrong on our end - please contact us for help adding your account.');
                return false;
                break;
            case 500: // balanced failed
                self.showGeneralError(true);
                self.generalError('Something went wrong on our end - please try again');
                return false;
                break;
            case 201: // success!
                self.balancedUri(response.data.uri);
                return true;
                break;
        }
    }

    self.getUri = function() {
        if (!self.valid()) return false;
        if (self.balancedUri()) return true;
        var data = {
            name: self.name.value(),
            account_number: self.accountNumber.value(),
            routing_number: self.routingNumber.value(),
            type: self.type.value()
        }
        self.showGeneralError(false);
        balanced.bankAccount.create(data, self.responseHandler);
        return false;
    }
}
