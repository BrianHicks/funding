function BankAccountModel() {
    var self = this;

    self.routingNumber = ko.observable();
    self.accountNumber = ko.observable();
    self.name = ko.observable();
}

function AddForm() {
    var self = this;

    self.bankAccount = new BankAccountModel();
}
