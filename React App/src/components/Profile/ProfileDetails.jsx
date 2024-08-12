import React from "react";
import { Button, Image } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { getUser } from "../../hooks/user.actions";

function ProfileDetails(props) {
  const { user } = props;
  const auth_user = getUser();

  const navigate = useNavigate();

  if (!user) {
    return <div>loading...</div>;
  }

  return (
    <div>
      <div className="d-flex flex-row border-bottom p-5">
        <Image
          src={user.avatar}
          roundedCircle
          width={120}
          height={120}
          className="me-5 border border-primary border-2"
        />
        <div className="d-flex flex-column justify-content-start align-self-center mt-2">
          <p className="fs-4 m-0">{user.username}</p>
          <p>{user.name}</p>
          <p className="fs-5">{user.bio ? user.bio : "(No bio.)"}</p>
          <p className="fs-6">
            { user.posts_count > 0 && <small>{user.posts_count} posts</small>}  
          </p>
          { auth_user.id === user.id && ( 
            <Button
            variant="primary"
            size="sm"
            className="w-100"
            onClick={() => navigate(`/profile/${user.id}/edit/`)}
          >
            Edit Profile
          </Button>
          )} 
          
        </div>
      </div>
    </div>
  );
}
export default ProfileDetails;
