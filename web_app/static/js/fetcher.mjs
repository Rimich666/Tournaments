const submitForm = (url, formData, onSuccess, onError)=>{
  fetch(url,{
    method: 'POST',
    body: formData,
    /*headers: {
      'Content-Type': 'multipart/form-data',
    }*/
  })
    .then((response)=>{
      if (response.ok) {
        return response;
      }
      throw response
      /*throw `status: ${response.status},
        statusText: ${response.statusText}`;*/
    })
    .then(onSuccess)
    .catch(onError);
};

export {submitForm};