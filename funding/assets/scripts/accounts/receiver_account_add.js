function BankAccountModel() {
    var self = this;

    self.routingNumber = new RoutingNumberModel();
    self.accountNumber = new AccountNumberModel();
    self.name = ko.observable();
}

function AddForm() {
    var self = this;

    self.bankAccount = new BankAccountModel();
}
