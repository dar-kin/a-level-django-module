function validateOrder(form) {
  var amount = form["amount"].value;
  if (amount <= 0) {
    const label = document.createElement('div');
    label.textContent = "Invalid amount";
    form.appendChild(label);
    form["amount"].after(label)
    return false;
  }
  form.submit()
}
