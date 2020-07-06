import React, { Component } from "react"; // React
import ReactFC from "react-fusioncharts"; // Fusion charts component
import FusionCharts from "fusioncharts"; // Fusion charts library
import TimeSeries from "fusioncharts/fusioncharts.timeseries"; // Chart type
import FusionTheme from "fusioncharts/themes/fusioncharts.theme.fusion"; // Theme
import { Dimmer, Loader, Segment } from "semantic-ui-react";

ReactFC.fcRoot(FusionCharts, TimeSeries, FusionTheme);

class MarketOverview extends Component {
    constructor(props) {
        super(props)

        // Obtaining data
        this.dataFetch = fetch("https://api.steamscout.com/market_overview")
        .then(res => res.json())
        .then(
            (result) => {
                for (let i = 0; i < result.length - 1; i++) {
                result[i + 1].push(result[i][4])
                }

                return result
            },
            (error) => {
                throw new Error(error)
            }
        )

        // Schema for data
        this.schemaFetch = [{
            "name": "Date",
            "type": "date",
            "format": "%Y-%m-%d"
        }, {
            "name": "Volume",
            "type": "number",
        }, {
            "name": "High",
            "type": "number",
        }, {
            "name": "Low",
            "type": "number",
        }, {
            "name": "Close",
            "type": "number",
        }, {
            "name": "Open",
            "type": "number",
        }]

        // Format of chart
        this.dataSource = {
            caption: {
              text: "Steam Market Item Value"
            },
            chart: {
              multicanvas: false,
              theme: "fusion"
            },
            yaxis: [
              {
                plot: [
                 {
                   value: "Volume",
                   type: "column"
                 }
                ],
              },
              {
                plot: [
                  {
                    value: {
                      open: "Open",
                      high: "High",
                      low: "Low",
                      close: "Close"
                    },
                    type: "candlestick"
                  }
                ],
                format: {
                  prefix: "$"
                },
              }
            ],
            navigator: {
              enabled: 0
            }
          };

          // Look of chart
          this.state = {
            timeseriesDs: {
              type: "timeseries",
              renderAt: "container",
              width: "100%",
              height: "500",
              dataSource: this.dataSource
            }
          };
    }

    componentDidMount() {
        Promise.all([this.dataFetch, this.schemaFetch]).then(res => {
            const data = res[0];
            const schema = res[1];
            const fusionTable = new FusionCharts.DataStore().createDataTable(
              data,
              schema
            );
            const timeseriesDs = Object.assign({}, this.state.timeseriesDs);
            timeseriesDs.dataSource.data = fusionTable;
            this.setState({
              timeseriesDs
            });
          });
    }

    render() {
        return (
            <Segment>
              {this.state.timeseriesDs.dataSource.data ? (
                <ReactFC {...this.state.timeseriesDs} />
              ) : (
                <Dimmer active inverted>
                    <Loader size='mini'>Loading Steam Market Overview...</Loader>
                </Dimmer>
              )}
            </Segment>
          );
      }
}

export default MarketOverview;
