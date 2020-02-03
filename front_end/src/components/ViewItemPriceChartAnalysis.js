import React from "react";
import FusionCharts from "fusioncharts";
import TimeSeries from "fusioncharts/fusioncharts.timeseries";
import ReactFC from "react-fusioncharts/lib/ReactFC";
import axios from 'axios';

ReactFC.fcRoot(FusionCharts, TimeSeries);

class ChartViewer extends React.Component {
  constructor(props) {
    super(props);

    const item_name = this.props.item_name

    this.dataFetch =
      axios
      .get("/view_item_price_history_chart", {
        params: {
          item_name,
        },
      })

    this.schemaFetch = [{
      "name": "Time",
      "type": "date",
      "format": "%-m/%-d/%Y %H:%M:%S"
    }, {
      "name": "Price",
      "type": "number"
    }, {
      "name": "Volume",
      "type": "number"
    }, {
      "name": "RSI",
      "type": "number"
    }, {
      "name": "MACD",
      "type": "number"
    }];

    this.dataSource = {
      chart: {},
      yaxis: [
        {
          plot: {
            connectNullData: '1',
            value: "Price",
            type: "msline"
          },
          title: "Price",
          format: {
            prefix: "$"
          }
        },
        {
          plot: {
            value: "Volume",
            type: "column"
          },
          title: "Volume"
        },
        {
          plot: {
            value: "RSI",
            type: "msline"
          },
            title: "RSI"
        },
        {
          plot: {
            value: "MACD",
            type: "column"
          },
            title: "MACD"
        }
      ]
    };
    this.state = {
      timeseriesDs: {
        type: "timeseries",
        renderAt: "container",
        width: "100%",
        height: "100%",
        dataSource: this.dataSource
      }
    };
  }

  componentDidMount() {
    Promise.all([this.dataFetch, this.schemaFetch]).then(res => {
      const data = res[0].data.price_history;
      const schema = res[1];
      const fusionTable = new FusionCharts.DataStore().createDataTable(
        data,
        schema
      );
      const timeseriesDs = Object.assign({}, this.state.timeseriesDs);
      timeseriesDs.dataSource.data = fusionTable;
      this.setState({
        timeseriesDs,
      });
    });
  }

  render() {
    return (
      <div>
        {this.state.timeseriesDs.dataSource.data ? (
          <ReactFC {...this.state.timeseriesDs} />
        ) : (
          "loading"
        )}
      </div>
    );
  }
}

export default ChartViewer;
