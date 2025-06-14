 
SCRIPT 1 (playerController.cs) 
 
 
using System; 
using UnityEngine; 
using UnityEngine.InputSystem; 
 
public class playerController : MonoBehaviour 
{ 
    public float walkspeed = 5f; 
    public float runspeed = 10f; 
    public float Airwalkspeed = 3f; 
    public float JumpImpulse = 10f; 
    Vector2 moveInput; 
    TouchingDirection direction; 
    Damageable Damageable; 
    Vector2 knockBackVelocity; 
 
    public float CurrentMoveSpeed 
    { 
        get 
        { 
            if (CanMove) 
            { 
                if (IsMoving && !direction.IsOnWall) 
                { 
                    if (direction.IsGrounded) 
                    { 
                        if (IsRunning) 
                        { 
                            return runspeed; 
                        } 
                        else 
                        { 
                            return walkspeed; 
                        } 
                    } 
                    else 
                    { 
                        return Airwalkspeed; 
                    } 
                } 
                else 
                { 
                    return 0; 
                } 
            } 
            else 
            { 
                return 0; 
            } 
             
        } 
 
    } 
     
     
    [SerializeField] 
    private bool _isMoving = false; 
     
    public bool IsMoving { get 
        {    
            return _isMoving; 
        }  
        private set 
        { 
            _isMoving = value; 
            animator.SetBool(AnimationStrings.IsMoving, value); 
        }  
    } 
     
    [SerializeField] 
    private bool _isRunning = false; 
 
    public bool IsRunning 
    { 
        get 
        { 
            return _isRunning; 
        } 
        set 
        { 
            _isRunning = value; 
            animator.SetBool(AnimationStrings.IsRunningPressed, value); 
        } 
    } 
 
    public bool _isFacingRight = true; 
    public bool IsFacingRight { get 
        { 
            return _isFacingRight;  
        }         
         
        private set  
        { 
            if (_isFacingRight != value) 
            { 
                transform.localScale *= new Vector2(-1,1); 
            } 
             
             
            _isFacingRight = value; 
        }  
    } 
 
    public bool CanMove  
    {  
        get  
        { 
 
            return animator.GetBool(AnimationStrings.canMove); 
        }  
    } 
 
    public bool IsAlive 
    { 
        get 
        { 
            return animator.GetBool(AnimationStrings.IsAlive); 
        } 
    } 
 
     
 
    Rigidbody2D rb; 
    Animator animator; 
    private void Awake() 
    { 
        rb = GetComponent<Rigidbody2D>(); 
        animator = GetComponent<Animator>(); 
        direction = GetComponent<TouchingDirection>(); 
        Damageable = GetComponent<Damageable>(); 
    } 
 
 
    private void FixedUpdate() 
    { 
        if (!Damageable.LockVelocity) //if we are hit, dont let any input affect movement 
        { 
            rb.linearVelocity = new Vector2(moveInput.x * CurrentMoveSpeed, rb.linearVelocity.y); //dont need to multiply 
by Time.fixedDeltaTime because velocity handles that 
            animator.SetFloat(AnimationStrings.Yvelocity, rb.linearVelocity.y); 
             
        } 
        else 
        { 
            rb.AddForce(knockBackVelocity * Time.deltaTime); //needs to be here because it's physics 
        } 
    } 
 
    public void OnMove(InputAction.CallbackContext context) 
    { 
        moveInput = context.ReadValue<Vector2>(); 
 
        if (IsAlive) 
        { 
            IsMoving = moveInput != Vector2.zero; 
 
            SetFacingDirection(moveInput); 
        } 
        else 
        { 
            IsMoving = false; 
        } 
    } 
 
 
    private void SetFacingDirection(Vector2 moveInput) 
    { 
        if (moveInput.x > 0 && !IsFacingRight) 
        { 
            IsFacingRight = true; 
        } 
        else if (moveInput.x < 0 && IsFacingRight) 
        { 
            IsFacingRight = false; 
        } 
    } 
 
    public void onRun(InputAction.CallbackContext context) 
    { 
        if (context.started) 
        { 
            IsRunning = true; 
        } 
        else if (context.canceled) 
        { 
            IsRunning = false; 
        } 
 
    } 
 
    public void OnJump(InputAction.CallbackContext context) 
    { 
        if (context.started && direction.IsGrounded && CanMove) 
        { 
            animator.SetTrigger(AnimationStrings.jump); 
            rb.linearVelocity = new Vector2(rb.linearVelocity.x, JumpImpulse); 
        } 
    } 
 
    public void OnAttack(InputAction.CallbackContext context) 
    { 
        if(context.started) 
        { 
            animator.SetTrigger(AnimationStrings.attack); 
        } 
    } 
 
    public void OnHit(int damage, Vector2 knockback) 
    { 
        rb.linearVelocity = new Vector2(knockback.x, rb.linearVelocity.y + knockback.y); //this line basically does 
nothing, it does not affect the x direction for some reason 
        knockBackVelocity = knockback; //set the new variable, put it in AddForce in FixedUpdate 
    } 
} 
 
 
SCRIPT 2 (Knight.cs) 
 
using System; 
 
using UnityEngine; 
 
public class Knight : MonoBehaviour 
{ 
    public float walkspeed = 3f; 
    public DetectionZone zone; 
 
    Rigidbody2D rb; 
    TouchingDirection Direction; 
    Animator animator; 
 
    public enum WalkDirection {Right, Left}; 
 
    private WalkDirection _walkDirection; 
    private Vector2 WalkDirectionVector; 
 
    public WalkDirection WalkDir 
    { 
        get { return _walkDirection; } 
        set { 
            if (_walkDirection != value) 
            { 
                gameObject.transform.localScale = new Vector2(gameObject.transform.localScale.x * -1, 
gameObject.transform.localScale.y); 
 
                if (value == WalkDirection.Right) 
                { 
                    WalkDirectionVector = Vector2.right; 
                }else if (value == WalkDirection.Left) 
                { 
                    WalkDirectionVector = Vector2.left; 
                } 
            } 
            _walkDirection = value; } 
    } 
 
    public bool _hasTarget = false; 
 
    public bool HasTarget { get 
        { 
            return _hasTarget; 
        } 
        private set  
        { 
            _hasTarget = value; 
            animator.SetBool(AnimationStrings.HasTarget, value); 
        }  
    } 
 
    public bool CanMove 
    { 
        get 
        { 
            return animator.GetBool(AnimationStrings.canMove); 
        } 
 
    } 
 
    private void Awake() 
    { 
        rb = GetComponent<Rigidbody2D>(); 
        Direction = GetComponent<TouchingDirection>(); 
        animator = GetComponent<Animator>(); 
    } 
 
    private void Update() 
    { 
        HasTarget = zone.detectedColliders.Count > 0; 
    } 
    void FixedUpdate() 
    { 
        if(Direction.IsGrounded && Direction.IsOnWall) 
        { 
            FlipDirection(); 
        } 
        if (CanMove) 
        { 
            rb.linearVelocity = new Vector2(walkspeed * WalkDirectionVector.x, rb.linearVelocity.y); 
        } 
        else 
        { 
            rb.linearVelocity = new Vector2(0, rb.linearVelocity.y); 
        } 
    } 
 
    private void FlipDirection() 
    { 
        if (WalkDir == WalkDirection.Right) 
        { 
            WalkDir = WalkDirection.Left; 
        } 
        else if (WalkDir == WalkDirection.Left) 
        {  
            WalkDir = WalkDirection.Right;  
        } 
        else 
        { 
            Debug.LogError("Current Walk Direction Not Valid"); 
        } 
 
    } 
} 
 
 
 
 
 
SCRIPT 3 (Damageable.CS) 
 
using UnityEngine; 
using UnityEngine.Events; 
 
 
public class Damageable : MonoBehaviour 
{ 
 
    public UnityEvent<int, Vector2> damageableHit; 
    Animator animator; 
    // Start is called once before the first execution of Update after the MonoBehaviour is created 
    [SerializeField] 
    private int _maxHealth=100; 
 
    public int MaxHealth 
    { 
        get 
        { 
            return _maxHealth; 
        } 
        set 
        { 
            _maxHealth = value; 
        } 
    } 
 
    [SerializeField] 
    private int _Health = 100; 
 
    public int Health 
    { 
        get 
        { 
            return _Health; 
        } 
        set 
        { 
            _Health = value; 
            if(_Health <= 0) 
            { 
                IsAlive = false; 
            } 
        } 
    } 
 
    private bool _IsAlive = true; 
    private bool IsInvincible = false; 
 
     
    private float timeSinceHit = 0; 
    public float invincibleTime = 0.25f; 
 
    public bool IsAlive { get  
        { 
            return _IsAlive; 
        } 
        set 
        { 
            _IsAlive = value; 
 
            animator.SetBool(AnimationStrings.IsAlive, value); 
        } 
    } 
 
    public bool LockVelocity 
    { 
        get 
        { 
            return animator.GetBool(AnimationStrings.LockVelocity); 
        } 
        set 
        { 
            animator.SetBool(AnimationStrings.LockVelocity, value); 
        } 
    } 
 
    private void Awake() 
    { 
        animator = GetComponent<Animator>(); 
 
    } 
 
    private void Update() 
    { 
        if(IsInvincible) 
        { 
            if(timeSinceHit > invincibleTime) 
            { 
                IsInvincible=false; 
                timeSinceHit = 0; 
            } 
 
            timeSinceHit += Time.deltaTime; 
        } 
 
    } 
 
    public bool Hit(int damage,Vector2 knockback) 
    { 
        if (IsAlive && !IsInvincible) 
        { 
            Health -= damage; 
            IsInvincible=true; 
 
            animator.SetTrigger(AnimationStrings.hit); 
            LockVelocity = true; 
 
            damageableHit?.Invoke(damage, knockback); 
             
            return true; 
        }else 
            { return false; } 
    } 
} 
 
 
SCRIPT 4 (Attack.CS) 
 
using UnityEngine; 
 
public class Attack : MonoBehaviour 
{ 
    public int attackdamage = 10; 
    public Vector2 knockback = Vector2.zero; 
 
    private void OnTriggerEnter2D(Collider2D collision) 
    { 
        Damageable damage = collision.GetComponent<Damageable>(); 
 
        if (damage != null) 
        { 
            bool GotHit  = damage.Hit(attackdamage, knockback); 
 
            if (GotHit) 
            { 
                Debug.Log(collision.name + " hit for " +  attackdamage); 
            } 
        } 
    } 
    // Update is called once per frame 
    void Update() 
    { 
         
    } 
} 
 
 
 
 
 
 
SCRIPT 5 (DetectionZone.CS) 
 
using UnityEngine; 
using System.Collections.Generic; 
 
public class DetectionZone : MonoBehaviour 
{ 
    public List<Collider2D> detectedColliders = new List<Collider2D>(); 
    Collider2D col; 
     
 
    private void Awake() 
    { 
        col = GetComponent<Collider2D>(); 
    } 
 
    private void OnTriggerEnter2D(Collider2D collision) 
    { 
        detectedColliders.Add(collision); 
    } 
private void OnTriggerExit2D(Collider2D collision) 
{ 
detectedColliders.Remove(collision); 
} 
} 
SCRIPT 6 (ParallaxEffect.CS) 
using UnityEngine; 
public class ParallaxEffect : MonoBehaviour 
{ 
public Camera cam; 
public Transform followTarget; 
Vector2 startingPosition; 
float startingZ; 
Vector2 camMoveSinceStart => (Vector2) cam.transform.position - startingPosition; 
float ZdistanceFromTarget => transform.position.z - followTarget.transform.position.z; 
float clippingPlane => cam.transform.position.z + (ZdistanceFromTarget > 0 ? cam.farClipPlane : 
cam.nearClipPlane); 
float parallaxFactor => Mathf.Abs(ZdistanceFromTarget) / clippingPlane; 
// Start is called once before the first execution of Update after the MonoBehaviour is created 
void Start() 
{ 
} 
startingPosition = transform.position; 
startingZ = transform.position.z; 
// Update is called once per frame 
void Update() 
{ 
Vector2 newPosition = startingPosition + camMoveSinceStart * parallaxFactor; 
transform.position = new Vector3(newPosition.x,newPosition.y,startingZ); 
} 
}