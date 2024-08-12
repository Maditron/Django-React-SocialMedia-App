import React, { useState, useEffect } from "react";
import { Button, Modal, Form, Dropdown } from "react-bootstrap";
import axiosService from "../../helpers/axios";
import Toaster from "../Toaster";
import { getUser } from "../../hooks/user.actions";



function UpdatePost(props) {
  const { post, refresh } = props;
  const [show, setShow] = useState(false);
  const [validated, setValidated] = useState(false);
  const [form, setForm] = useState({
    author: '',
    body: '',
  });
  
  useEffect(() => {
    if (post) {
      setForm({
        author: post.author.id,
        body: post.body
      });
    }
  }, [post]);
  
  
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const user = getUser();
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const [toastType, setToastType] = useState("");


  const handleSubmit = (event) => {
    event.preventDefault();
    const createPostForm = event.currentTarget;
    if (createPostForm.checkValidity() === false) {
      event.stopPropagation();
    }

    setValidated(true);
    const data = {
      author: user.id,
      body: form.body,
    };

    axiosService
      .put(`/post/${post.id}/`, data)
      .then(() => {
        handleClose();
        setToastMessage("Post Edited 🚀");
        setToastType("success");
        setShowToast(true);
        // setForm({});
        refresh();
      })
      .catch(() => {
        setToastMessage("An error occurred.");
        setToastType("danger");
      });
  };


  return (
    <>
    
      <Dropdown.Item onClick={handleShow}>Modify</Dropdown.Item>


      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton className="border-0">
          <Modal.Title>Edit Post</Modal.Title>
        </Modal.Header>
        <Modal.Body className="border-0">
          <Form noValidate validated={validated} onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Control
                name="body"
                value={form.body}
                onChange={(e) => setForm({ ...form, body: e.target.value })}
                as="textarea"
                rows={3}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="primary"
            onClick={handleSubmit}
            disabled={form.body === undefined}
          >
            Post
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
export default UpdatePost;
