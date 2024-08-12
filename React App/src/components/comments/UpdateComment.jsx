import React, { useState, useContext, useEffect } from "react";
import { Button, Modal, Form, Dropdown } from "react-bootstrap";
import axiosService from "../../helpers/axios";
import { Context } from "../layout";
import { getUser } from "../../hooks/user.actions";

function UpdateComment(props) {
  const { post, comment, refresh, postId } = props;
  const [show, setShow] = useState(false);
  const [validated, setValidated] = useState(false);
  const user = getUser();

  const [form, setForm] = useState({
    author: '',
    body: '',
    post: '',
  });

  useEffect(() => {
    if (comment){
      setForm({
        author: comment.author.id,
        body: comment.body,
        post: comment.post.id,
      })
    }
  }, [comment])

  const { toaster, setToaster } = useContext(Context);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);



  const handleSubmit = (event) => {
    event.preventDefault();
    const updateCommentForm = event.currentTarget;
    if (updateCommentForm.checkValidity() === false) {
      event.stopPropagation();
    }
    setValidated(true);
    const data = {
      author: user.id,
      body: form.body,
      post: postId,
    };
    axiosService
      .put(`/post/${postId}/comment/${comment.id}/`, data)
      .then(() => {
        handleClose();
        setToaster({
          type: "success",
          message: "Comment updated 🚀",
          show: true,
          title: "Success!",
        });
        refresh();
      })
      .catch((error) => {
        setToaster({
          type: "danger",
          message: "An error occurred.",
          show: true,
          title: "Comment Error",
        });
      });
  };



  return (
    <>

      <Dropdown.Item onClick={handleShow}>Modify</Dropdown.Item>


      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton className="border-0">
          <Modal.Title>Update Post</Modal.Title>
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
          <Button variant="primary" onClick={handleSubmit}>
            Modify
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
export default UpdateComment;
