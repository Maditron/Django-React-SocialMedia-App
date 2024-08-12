import React, { useState, useContext } from "react";
import { Form, Button, Image } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { useUserActions } from "../../hooks/user.actions";
import { Context } from "../layout";
import axios from "axios";

function UpdateProfileForm(props) {
  const { profile } = props;
  const navigate = useNavigate();
  const [validated, setValidated] = useState(false);
  const [form, setForm] = useState(profile);
  const [error, setError] = useState(null);
  const userActions = useUserActions();
  const [avatar, setAvatar] = useState();
  const [avatar2, setAvatar2] = useState();
  const { toaster, setToaster } = useContext(Context);




  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file){
        setAvatar2(URL.createObjectURL(file));
        setAvatar(e.target.files[0]); 
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const updateProfileForm = event.currentTarget;
    if (updateProfileForm.checkValidity() === false) {
      event.stopPropagation();
    }
    setValidated(true);
    const data = {
      username: form.username,
      email: form.email,
      first_name: form.first_name,
      last_name: form.last_name,
      bio: form.bio,
    };
    const formData = new FormData();

    Object.keys(data).forEach((key) => {
      if (data[key]) {
        formData.append(key, data[key]);
      }
    });

    if (avatar) {
      formData.append("avatar", avatar); 
    } 

    userActions
      .edit(formData, profile.id)
      .then(() => {
        setToaster({
          type: "success",
          message: "Profile updated successfully 🚀",
          show: true,
          title: "Profile updated",
        });
        navigate(-1);
      })
      .catch((err) => {
        if (err.message) {
          setError(err.request.response);
        }
      });
  };

  return (
    <Form
    encType="multipart/form-data"
      id="registration-form"
      className="border p-4 rounded"
      noValidate
      validated={validated}
      onSubmit={handleSubmit}
    >
      <Form.Group className="mb-3 d-flex flex-column">
        <Form.Label className="text-center">Avatar</Form.Label>
            <Image
            src={avatar2 || form.avatar}   
            roundedCircle
            width={120}
            height={120}
            className="m-2 border border-primary border-2
      align-self-center"
          />
        
        <Form.Control
          onChange={handleFileChange}
          className="w-50 align-self-center"
          type="file"
          size="sm"
        />
        <Form.Control.Feedback type="invalid">
          This file is required.
        </Form.Control.Feedback>
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Username</Form.Label>
        <Form.Control
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          required
          type="text"
          placeholder="Enter username"
        />
        <Form.Control.Feedback type="invalid">
          This file is required.
        </Form.Control.Feedback>
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Email</Form.Label>
        <Form.Control
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
          type="text"
          placeholder="Enter first name"
        />
        <Form.Control.Feedback type="invalid">
          This file is required.
        </Form.Control.Feedback>
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>First Name</Form.Label>
        <Form.Control
          value={form.first_name}
          onChange={(e) => setForm({ ...form, first_name: e.target.value })}
          required
          type="text"
          placeholder="Enter first name"
        />
        <Form.Control.Feedback type="invalid">
          This file is required.
        </Form.Control.Feedback>
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Last name</Form.Label>
        <Form.Control
          value={form.last_name}
          onChange={(e) => setForm({ ...form, last_name: e.target.value })}
          required
          type="text"
          placeholder="Enter last name"
        />
        <Form.Control.Feedback type="invalid">
          This file is required.
        </Form.Control.Feedback>
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Bio</Form.Label>
        <Form.Control
          value={form.bio || ''} 
          onChange={(e) => setForm({ ...form, bio: e.target.value })}
          as="textarea"
          rows={3}
          placeholder="A simple bio ... (Optional)"
        />
      </Form.Group>

      <div className="text-content text-danger">{error && <p>{error}</p>}</div>
      <Button variant="primary" type="submit">
        Save changes
      </Button>
    </Form>
  );
}
export default UpdateProfileForm;
