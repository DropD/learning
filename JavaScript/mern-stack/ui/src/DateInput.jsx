import React from "react";


function displayFormat(date) {
  return (date != null) ? date.toDateString() : ``;
}

function editFormat(date) {
  return (date != null) ? date.toISOString().substr(0, 10) : ``;
}

function unformat(str) {
  const val = new Date(str);
  return Number.isNaN(val.getTime()) ? null : val;
}

export default class DateInput extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: editFormat(props.value), focused: false, valid: true };
    this.onFocus = this.onFocus.bind(this);
    this.onChange = this.onChange.bind(this);
    this.onBlur = this.onBlur.bind(this);
  }

  onFocus() {
    this.setState({ focused: true });
  }

  onChange(event) {
    if (event.target.value.match(/^[\d-]*$/)) {
      this.setState({ value: event.target.value });
    }
  }

  onBlur(event) {
    const { onValidityChange, onChange } = this.props;
    const { value, valid: oldValid } = this.state;
    const dateValue = unformat(value);
    const valid = value === `` || dateValue != null;
    if (valid != oldValid && onValidityChange) {
      onValidityChange(event, valid);
    }
    this.setState({ focused: false, valid });
    if (valid) onChange(event, dateValue);
  }

  render() {
    const { value, focused, valid } = this.state;
    const { value: origValue, name } = this.props;
    const className = (!valid && !focused) ? 'invalid': null;
    const displayValue = (focused || !valid) ? value : displayFormat(origValue);
    return (
      <input
        type="text"
        size={20}
        name={name}
        className={className}
        value={displayValue}
        placeholder={focused ? 'yyy-mm-dd' : null}
        onFocus={this.onFocus}
        onBlur={this.onBlur}
        onChange={this.onChange}
      />
    );
  }
}

