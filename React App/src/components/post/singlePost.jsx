import React from "react";
import Layout from "../layout";
import { Row, Col } from "react-bootstrap";
import { useParams } from "react-router-dom";
import useSWR from "swr";
import { fetcher } from "../../helpers/axios";
import Post from "./Post";
import CreateComment from "../comments/CreateComments";
import Comment from "../comments/Comment";

// import Comment from "../components/comments/Comment";

function SinglePost() {
  const { postId } = useParams();
  const post = useSWR(`/post/${postId}/`, fetcher);
  const comments = useSWR(`/post/${postId}/comment/`, fetcher);

  return (
    <Layout hasNavigationBack={true}>
      {post.data ? (
        <Row className="justify-content-center">
          <Col sm={8}>
            <Post post={post.data} refresh={post.mutate} isSinglePost={true} />
            <CreateComment postId={post.data.id} refresh={comments.mutate} />
            {comments.data?.results.map((comment, index) => (
              <Comment key={index} postId={postId} refresh={comments.mutate} comment={comment} post={post} />
            ))}

          </Col>
        </Row>
      ) : (
        <div>Loading...</div>
      )}
    </Layout>
  );
}

export default SinglePost;
