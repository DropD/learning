import React from "react";


function format(num) {
  return num != null ? num.toString() : ``;
}

function unformat(str) {
  const val = parseInt(str, 10);
  return Number.isNaN(val) ? null : val;
}

export default class NumInput extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: format(props.value) };
    this.onChange = this.onChange.bind(this);
    this.onBlur = this.onBlur.bind(this);
  }

  onChange(event) {
    if (event.target.value.match(/^\d*$/)) {
      this.setState({ value: event.target.value });
    }
  }

  onBlur(event) {
    const { onChange } = this.props;
    const { value } = this.state;
    onChange(event, unformat(value));
  }

  render() {
    const { value } = this.state;
    return (
      <input type="text" {...this.props} value={value} onBlur={this.onBlur} onChange={this.onChange} />
    );
  }
}
