import React, { useState } from "react";
// import FetchTest from './About/FetchTest.js';
import './SignUp.css';

const InstructorQuesitons =  (props) => {
    return(
        <div>
            <h2>Additional questions for Instructors</h2>
            <form>
                <h4>Check all that apply. Do you identify as:</h4>
                <label for="coach">Coach</label>
                <input type="checkbox" name="coach" id="coach" onChange={props.handleSelectIdentify}/><br/>
                
                <label for="teacher">Teacher</label>
                <input type="checkbox" name="teacher" id="teacher" onChange={props.handleSelectIdentify}/><br/>
                
                <label for="facilitator">Facilitator</label>
                <input type="checkbox" name="facilitator" id="facilitator" onChange={props.handleSelectIdentify}/><br/>

                <label for="other">Other: Please List:</label>
                <input type="text" name="other" id="otherInstructor" onChange={props.handleSelectIdentify}/><br/>
            </form>
            <form>
                <h4>What do you need U-Impactify for?</h4>
                <label for="choice1">Conduct Lessons Live</label>
                <input type="checkbox" name="choice1" id="choice1" onChange={props.handleSelectChoice}/><br/>
                
                <label for="choice2">Handle Administrative Tasks</label>
                <input type="checkbox" name="choice2" id="choice2" onChange={props.handleSelectChoice}/><br/>
                
                <label for="choice3">Plan my lessons and sessions</label>
                <input type="checkbox" name="choice3" id="choice3" onChange={props.handleSelectChoice}/><br/>
            </form>
        </div>
    )
}


const SocialInitiativesQuestions = () => {
    return(
        <div>
        <h2>Additional questions for Social Initiatives</h2>
        <form>
            <h4>Check all that apply. Do you identify as:</h4>
            <label>Social entrepreneurs or intrapreneurs</label>
            <input type="checkbox" name="entreperneur" id="entreperneur"/><br/>
            
            <label>Worker at a charity or a non-profit organization</label>
            <input type="checkbox" name="charity" id="charity" /><br/>
            
            <label>Individual who wants to learn something new</label>
            <input type="checkbox" name="learner" id="learner" /><br/>

            <label>Other: Please List:</label>
            <input type="text" name="otherInitiativesCategory1" id="otherInitiativesCategory1" /><br/>
        </form>
        <form>
            <h4>What category does your company fits in?</h4>
            <label>Arts and Culture</label>
            <input type="checkbox" name="ArtsCulture" id="ArtsCulture" /><br/>
                
            <label for="teacher">Civic and Environmental</label>
            <input type="checkbox" name="Civic" id="Civic" /><br/>
                
            <label for="facilitator">Education</label>
            <input type="checkbox" name="Educaiton" id="Educaiton" /><br/>

            <label for="facilitator">Health Services</label>
            <input type="checkbox" name="Health" id="Health"/><br/>

            <label for="facilitator">International Relations and Development</label>
            <input type="checkbox" name="InternationalRelations" id="InternationalRelations" /><br/>

            <label for="facilitator">Social and Legal Services</label>
            <input type="checkbox" name="SocialLegalServices" id="SocialLegalServices"/><br/>

            <label for="other">Other: Please List:</label>
            <input type="text" name="otherInitiativesCategory2" id="otherInitiativesCategory2" /><br/>
        </form>
        <form>
            <h4>What do you want to learn more about? (select all that apply)</h4>
            <label for="coach">Accounting</label>
            <input type="checkbox" name="Accounting" id="Accounting"/><br/>
                
            <label for="teacher">Business</label>
            <input type="checkbox" name="Business" id="Business"/><br/>
                
            <label for="facilitator">Communication</label>
            <input type="checkbox" name="Communication" id="Communication"/><br/>

            <label for="facilitator">Design</label>
            <input type="checkbox" name="Design" id="Design"/><br/>

            <label for="facilitator">Finance</label>
            <input type="checkbox" name="Finance" id="Finance"/><br/>

            <label for="facilitator">Project Managament</label>
            <input type="checkbox" name="Project Managament" id="Project Managament"/><br/>

            <label for="other">Other: Please List:</label>
            <input type="text" name="otherInitiativesCategory3" id="otherInitiativesCategory3"/><br/>
        </form>
    </div>
    )
}

const UserTypeDeclaration = (props) => {
    return(
        <form>
            <h3>Are you joining as a Student or Instructor?</h3>
            <label for="Student">Student</label>
            <input type="radio" name="userType" id="Student" onChange={props.handleSelectType}/>

            <label for="Instructor">Instructor</label>
            <input type="radio" name="userType" id="Instructor" onChange={props.handleSelectType}/>

            <label for="Social Initiative">Social Initiative</label>
            <input type="radio" name="userType" id="Social Initiative" onChange={props.handleSelectType} />
            <br/>
        </form>
    )
}

const GenericQuestions = (props) => {
    return(
        <form>
            <label for="email">Email:</label><br/>
            <input type="text" name="email" placeholder="Email" 
            value={props.email} onChange={props.handleEmailChange}/><br/>

            <label for="Username">Username:</label><br/>
            <input type="text" name="username" placeholder="username" 
            value={props.username} onChange={props.handleUsernameChange}/><br/>

            <label for="password">Password:</label><br/>
            <input type="password" name="password" placeholder="password" 
            value={props.password} onChange={props.handlePasswordChange}/><br/>
        </form>
    )
}

function SignUp() {
    const [email, setEmail] = useState('')
    const [type, setType] = useState('')
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [identify, setIdentify] = useState([])
    const [other, setOther] = useState('')
    const [choice, setChoice] = useState('')

    const handleSelectIdentify = (event) => {
        setIdentify(identify.concat(event.target.name))
        alert(`${event.target.name} is chosen`)
        console.log(identify)
    } 

    const handleSelectChoice = (event) =>{
        setChoice(event.target.name)
    }

    const handleUsernameChange = (event) => {
        setUsername(event.target.value)
    }

    const handlePasswordChange = (event) => {
        setPassword(event.target.value)
    }
    
    const handleSelectType = (event) => {
        if(type === ''){
            setType(event.target.id)
            alert(`${event.target.id} is chosen`)
            //console.log(`${event.target.value}`)
        }else{
            alert(`Now chosen:${event.target.id}, changed from: ${type}`)

            setType(event.target.id)
        }
    }

    const handleEmailChange = (event) => {
        setEmail(event.target.value)
        console.log(`email is: ${email}`)
    }

    const handleSignUp = (event) => {
        console.log("signed in?")
    }

    return (
        <div>
            <p className="SignUp-colour">Sign Up</p>
            <h1>Create an Account</h1>
            <GenericQuestions 
            email={email} handleEmailChange={handleEmailChange}
            username={username} handleUsernameChange={handleUsernameChange}
            password={password} handlePasswordChange={handlePasswordChange}
            />
            <UserTypeDeclaration handleSelectType={handleSelectType}/>
            <InstructorQuesitons
            handleSelectIdentify={handleSelectIdentify}
            handleSelectChoice={handleSelectChoice}/>
            <SocialInitiativesQuestions/>
            <input type="submit" value="Sign Up" onSubmit={handleSignUp}/>
        </div>
    );
}

export default SignUp;