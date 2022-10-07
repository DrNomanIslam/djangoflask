import React, { Component } from "react"
import axios from 'axios';
import "bootstrap/dist/css/bootstrap.min.css";
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';


class App extends Component {

  state = {
    details: [],
    authors: "",
    title: "",
    journal: "",
    year_of_publication: "",
    vol:"",
    issue:"",
    pp:""
  };


  handleClose = () => {
    this.setState({show: false});
  }
  
  handleShow = () => {
    this.setState({show: true});
  }


  handleInput = (e) => {
    this.setState({
        [e.target.id]: e.target.value,
    });
  }
  
  componentDidMount() {  
    let data;
    axios.get('http://localhost:8000/api/')
    .then(res => {
        data = res.data;
        console.log(data);
        this.setState({
            details : data    
        });
    })
    .catch(err => {})
  }


  render() {
    return(
      <div className="container jumbotron ">
        <br></br><br></br><br></br>
        <div>
      <Button variant="primary" onClick={this.handleShow}>
        New Publication
      </Button>

      <Modal show={this.state.show} onHide={this.handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>New Publication</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>
            Authors:
          </div>
          <div>
            <div class="col">Title: </div>
            <div class="col">
              <input onChange={this.handleInput} type="text" id="title" class="form-Control"></input>
            </div>
          </div>
          <div>
          <div class="col">
          Journal: </div><div class="col"><input onChange={this.handleInput} type="text" id="journal" class="form-Control"></input></div>
          </div>
          <div>
          <div class="col">Year: </div>
          <div class="col">
          <input type="text" id="year_of_publication" onChange={this.handleInput} class="form-Control"></input>
          </div>
          </div>

          <div>
          <div class="col">Volume: </div>
          <div class="col">
          <input type="text" id="vol" onChange={this.handleInput} class="form-Control"></input>
          </div>
          </div>

          <div>
          <div class="col">
          Issue: 
          </div>
          <div class="col">
          <input type="text" id="issue" class="form-Control" onChange={this.handleInput}></input>
          </div>
          </div>
          <div>
          <div class="col">
          Page #: </div>
          <div>
          <input type="text" id="pp" class="form-Control" onChange={this.handleInput}></input>
          </div>
          </div>

          
          
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={this.handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={this.handleClose}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>



      
      </div>


        <br></br><br></br><br></br><br></br>
        <p align="center"><b>List of Publications</b></p>

            <div class="container-sm">
              <div class="row alert alert-success">
                  <div class="col">
                    Author
                  </div>
                  <div class="col">
                    Title
                  </div>

                  <div class="col">
                    Journal
                  </div>

                  <div class="col">
                    Year of Publication
                  </div>

                  <div class="col">
                    Volume
                  </div>
                  <div class="col">
                    Issue
                  </div>

                  <div class="col">
                    pp.
                  </div>
              </div>

            {this.state.details.map((d) =>  (            
            <div class="row">
                  <div class="col">
                        {d.authors[0][1]}
                  </div>
              
                  <div class="col">
                        {d.title}
                  </div>
                  <div class="col">
                        {d.journal}
                  </div>

                  <div class="col">
                        {d.year_of_publication}
                  </div>
                  <div class="col">
                        {d.volume}
                  </div>

                  <div class="col">
                        {d.issue}
                  </div>
                  <div class="col">
                        {d.pp}
                  </div>
            </div>
            
            )          
        )}
        </div>
      </div>
      );
  }

}


export default App;