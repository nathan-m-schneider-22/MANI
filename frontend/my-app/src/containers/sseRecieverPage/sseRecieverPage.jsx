import React from 'react';
import axios from 'axios'

class sseRecieverPage extends React.Component {
constructor(){
    super()
      this.state = {
        data: []
      };
    this.eventSource = new EventSource("http://localhost:5000/events");
  }

  componentDidMount() {

      this.eventSource.addEventListener("dataUpdate", e =>
      this.updateState(JSON.parse(e.data))
    );

  axios.get("http://localhost:5000/",
  {headers: {'Access-Control-Allow-Origin': '*'}
  })
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            data: result.data
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }
     updateState(newState) {
        console.log("Server side event recieved at",new Date())
        console.log(newState)
      }
  render() {
    return (
     <p>TBD</p>
    )
}
}
export default sseRecieverPage;
